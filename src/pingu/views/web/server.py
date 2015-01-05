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

@app.route("/servers", methods = ("GET",))
@quorum.ensure("servers.list")
def list_servers():
    servers = models.Server.find_i()
    return flask.render_template(
        "server/list.html.tpl",
        link = "servers",
        sub_link = "list",
        servers = servers
    )

@app.route("/servers/new", methods = ("GET",))
@quorum.ensure("servers.new")
def new_server():
    return flask.render_template(
        "server/new.html.tpl",
        link = "servers",
        sub_link = "create",
        server = {},
        errors = {}
    )

@app.route("/servers", methods = ("POST",))
@quorum.ensure("servers.new")
def create_server():
    # creates the new server, using the provided arguments and
    # then saves it into the data source, all the validations
    # should be ran upon the save operation
    server = models.Server.new()
    try: server.save()
    except quorum.ValidationError as error:
        return flask.render_template(
            "server/new.html.tpl",
            link = "servers",
            sub_link = "create",
            server = error.model,
            errors = error.errors
        )

    # redirects the user to the show page of the server that
    # was just created
    return flask.redirect(
        flask.url_for("show_server", name = server.name)
    )

@app.route("/servers/<name>", methods = ("GET",))
@quorum.ensure("servers.show")
def show_server(name):
    server = models.Server.get_i(name = name)
    return flask.render_template(
        "server/show.html.tpl",
        link = "servers",
        sub_link = "info",
        server = server
    )

@app.route("/servers/<name>/edit", methods = ("GET",))
@quorum.ensure("servers.edit")
def edit_server(name):
    server = models.Server.get_i(name = name)
    return flask.render_template(
        "server/edit.html.tpl",
        link = "servers",
        sub_link = "edit",
        server = server,
        errors = {}
    )

@app.route("/servers/<name>/edit", methods = ("POST",))
@quorum.ensure("servers.edit")
def update_server(name):
    # finds the current server and applies the provided
    # arguments and then saves it into the data source,
    # all the validations should be ran upon the save operation
    server = models.Server.get_i(name = name)
    server.apply()
    try: server.save()
    except quorum.ValidationError as error:
        return flask.render_template(
            "server/edit.html.tpl",
            link = "servers",
            sub_link = "edit",
            server = error.model,
            errors = error.errors
        )

    # redirects the user to the show page of the server that
    # was just updated
    return flask.redirect(
        flask.url_for("show_server", name = name)
    )

@app.route("/servers/<name>/delete", methods = ("GET", "POST"))
@quorum.ensure("servers.delete")
def delete_server(name):
    server = models.Server.get_i(name = name)
    server.delete()
    return flask.redirect(
        flask.url_for("list_servers")
    )

@app.route("/servers/<name>/log", methods = ("GET",))
@quorum.ensure("log.list")
def list_log(name):
    server = models.Server.get_i(name = name)
    return flask.render_template(
        "server/log.html.tpl",
        link = "servers",
        sub_link = "log",
        server = server
    )

@app.route("/servers/<name>/log.json", methods = ("GET",), json = True)
@quorum.ensure("log.list", json = True)
def list_log_json(name):
    object = quorum.get_object(alias = True, find = True)
    log = models.Log.find_i(map = True, name = name, **object)
    return log

@app.route("/<name>", methods = ("GET",))
def profile_server(name):
    server = models.Server.get(name = name)
    return flask.render_template(
        "site/server_profile.html.tpl",
        link = "servers",
        sub_link = "profile",
        server = server
    )

@app.route("/<name>/badge", methods = ("GET",))
def badge_server(name):
    server = models.Server.get(name = name)
    data = server.badge()

    # returns the "binary" response as a png based image (the "just
    # generated badge image)
    return flask.Response(
        data,
        mimetype = "image/png"
    )
