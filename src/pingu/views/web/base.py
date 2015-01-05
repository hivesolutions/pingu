#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Pingu System
# Copyright (C) 2008-2015 Hive Solutions Lda.
#
# This file is part of Hive Pingu System.
#
# Hive Pingu System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Pingu System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Pingu System. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

from pingu import models

from pingu.main import app
from pingu.main import flask
from pingu.main import quorum

@app.route("/home", methods = ("GET",))
def home():
    return flask.render_template(
        "site/index.html.tpl",
        link = "home"
    )

@app.route("/docs", methods = ("GET",))
@app.route("/docs/api", methods = ("GET",))
def docs_api():
    return flask.render_template(
        "site/docs_api.html.tpl",
        link = "home"
    )

@app.route("/", methods = ("GET",))
@app.route("/index", methods = ("GET",))
@quorum.ensure("index")
def index():
    return flask.render_template(
        "index.html.tpl",
        link = "home"
    )

@app.route("/about", methods = ("GET",))
@quorum.ensure("about")
def about():
    return flask.render_template(
        "about.html.tpl",
        link = "about"
    )

@app.route("/pending/<username>", methods = ("GET",))
def pending(username):
    account = models.Account.get(username = username)
    return flask.render_template(
        "pending.html.tpl",
        account = account
    )

@app.route("/resend/<username>", methods = ("GET",))
def resend(username):
    # starts the confirmation process for the account this should
    # start sending the email to the created account
    account = models.Account.get(username = username, build = False)
    account.confirm()

    return flask.render_template(
        "pending.html.tpl",
        account = account
    )

@app.route("/confirm/<confirmation>", methods = ("GET",))
def confirm(confirmation):
    # tries to set the account with the provided confirmation
    # code as enabled (only in case the confirmation code is valid)
    models.Account.confirmed(confirmation)

    return flask.render_template(
        "confirmed.html.tpl"
    )

@app.route("/signin", methods = ("GET",))
def signin():
    return flask.render_template(
        "signin.html.tpl"
    )

@app.route("/signin", methods = ("POST",))
def login():
    username = quorum.get_field("username")
    password = quorum.get_field("password")
    try: account = models.Account.login(username, password)
    except quorum.OperationalError as error:
        return flask.render_template(
            "signin.html.tpl",
            username = username,
            error = error.message
        )

    # updates the current user (name) in session with
    # the username that has just be accepted in the login
    flask.session["username"] = account.username
    flask.session["tokens"] = account.tokens
    flask.session["instance_id"] = account.instance_id
    flask.session["nav_data"] = None

    # makes the current session permanent this will allow
    # the session to persist along multiple browser initialization
    flask.session.permanent = True

    return flask.redirect(
        flask.url_for("index")
    )

@app.route("/signout", methods = ("GET", "POST"))
def logout():
    if "username" in flask.session: del flask.session["username"]
    if "tokens" in flask.session: del flask.session["tokens"]
    if "instance_id" in flask.session: del flask.session["instance_id"]
    if "nav_data" in flask.session: del flask.session["nav_data"]

    return flask.redirect(
        flask.url_for("signin")
    )
