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

import json
import time

from pingu import models

from pingu.main import app
from pingu.main import flask
from pingu.main import quorum

# loads the manifest information json and retrieves
# the various partial values from it to be used
# for authentication and configuration of the app
heroku_conf = quorum.load_json("heroku", "addon-manifest.json")
api = heroku_conf.get("api", {})
username_h = heroku_conf.get("id", None)
password_h = api.get("password", None)
salt_h = api.get("sso_salt", None)
navbar_h = api.get("navbar", None)

quorum.confs("salt_h", salt_h)

def create_servers_h(heroku_id, account, sleep_time = 3.0):
    # sleeps for a while so that no collision with the remote
    # server occurs (the application must be registered already)
    time.sleep(sleep_time)

    # retrieves the current instance id to be used
    # from the account structure provided, then encodes
    # the provided heroku id into url encode
    instance_id = account.instance_id
    heroku_id_e = quorum.legacy.quote(heroku_id)

    # creates the complete url string from the username,
    # password and heroku id to be used and the opens the
    # url reading its data
    url = "https://%s:%s@api.heroku.com/vendor/apps/%s" % (username_h, password_h, heroku_id_e)
    try:
        remote = quorum.legacy.urlopen(url)
        try: data = remote.read()
        finally: remote.close()
    except:
        data = "{}"

    # loads the json structure from the data and obtains the
    # owner email and the various domains contained in it
    object = json.loads(data)
    owner_email = object.get("owner_email", "notset@heroku.com")
    domains = object.get("domains", [])

    # sets the owner email of the instance as the email in the
    # account and the saves the account
    account.email = owner_email
    account.save()

    # creates the list that will be used to store the various
    # servers to be created from the domains
    servers = []

    # iterates over all the domains to insert the associated servers
    # into the data source
    for domain in domains:
        # creates the url string from the domain, note that the url to
        # be used is the root one (index page)
        url = "http://" + domain + "/"

        # creates the structure to be used as the server description
        # using the values provided as parameters and then saves it
        # into the data source
        server = dict(
            enabled = True,
            instance_id = instance_id,
            name = domain,
            url = url,
            description = domain
        )
        server = models.Server.new(model = server)
        server.save()

        # creates a task for the server that has just been created
        # this tuple is going to be used by the scheduling thread
        # then schedules for execution in next iteration (immediately)
        task = models.Task(server)
        task.schedule()

        # adds the servers structure to the list of servers that
        # have been created
        servers.append(server)

    # returns the complete set of servers that have been created
    # to the caller method (for reference)
    return servers

def get_navbar_h():
    global navbar_h
    if navbar_h: return navbar_h
    server = quorum.legacy.urlopen("http://nav.heroku.com/v1/providers/header")
    try: data = server.read()
    finally: server.close()
    navbar_h = data
    return navbar_h

@app.route("/heroku/resources", methods = ("POST",))
@quorum.ensure_auth(username_h, password_h, json = True)
def provision():
    # retrieves the complete set of data from the request
    # and then unpacks it into the expected attributes
    heroku_id = quorum.get_field("heroku_id")
    plan = quorum.get_field("plan")

    # creates the heroku account with the unpacked values from the
    # provided message
    account = models.Account.create_heroku(heroku_id, plan = plan)

    # schedules the execution of the server creation for
    # the current provision, this will be deferred so that
    # the call is only made after provision is complete
    quorum.run_back(
        create_servers_h,
        args = (heroku_id, account)
    )

    return flask.Response(
        json.dumps({
            "id" : heroku_id,
            "config" : {
                "PINGU_API_KEY" : account.api_key,
                "PINGU_APP_ID" : heroku_id
            }
        }),
        mimetype = "application/json"
    )

@app.route("/heroku/resources/<id>", methods = ("DELETE",))
@quorum.ensure_auth(username_h, password_h, json = True)
def deprovision(id):
    account = models.Account.get(username = id)
    account.delete()

    return "ok"

@app.route("/heroku/resources/<id>", methods = ("PUT",))
@quorum.ensure_auth(username_h, password_h, json = True)
def plan_change(id):
    plan = quorum.get_field("plan")

    account = models.Account.get(username = id)
    account.plan = plan
    account.save()

    return "ok"

@app.route("/sso/login", methods = ("POST",))
def sso_login():
    # retrieves the various parameters provided by the
    # caller post operation to be used in the construction
    # of the response and security validations
    id = quorum.get_field("id")
    timestamp = quorum.get_field("timestamp")
    token = quorum.get_field("token")
    nav_data = quorum.get_field("nav-data")

    # runs the sso login for the provided arguments and retrieves
    # the account that has just been logged in
    account = models.Account.sso_login(id, timestamp, token, nav_data)

    # retrieves the contents to be use in the navigation bar for the
    # heroku session
    navbar_h = get_navbar_h()

    # updates the current user (name) in session with
    # the username that has just be accepted in the login
    flask.session["username"] = account.username
    flask.session["tokens"] = account.tokens
    flask.session["instance_id"] = account.instance_id
    flask.session["nav_data"] = navbar_h

    # makes the current session permanent this will allow
    # the session to persist along multiple browser initialization
    flask.session.permanent = True

    # creates a new redirect request and uses it to create
    # the response object that is set with the cookie value
    # to be used by heroku navigation bar
    redirect = flask.redirect(
        flask.url_for("list_servers")
    )
    response = flask.make_response(redirect)
    response.set_cookie("heroku-nav-data", value = nav_data)
    return response
