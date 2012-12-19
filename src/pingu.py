#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Pingu System
# Copyright (C) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import uuid
import json
import time
import flask
import atexit
import urllib
import thread
import hashlib
import httplib
import smtplib
import datetime
import urlparse
import cStringIO

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

import email.mime.multipart
import email.mime.text

import config
import models
import quorum

SECRET_KEY = "kyjbqt4828ky8fdl7ifwgawt60erk8wg"
""" The "secret" key to be at the internal encryption
processes handled by flask (eg: sessions) """

PASSWORD_SALT = "pingu"
""" The salt suffix to be used during the encoding
of the password into an hash value """

TASKS = ()
""" The set of tasks to be executed by ping operations
this is the standard hardcoded values """

MONGO_DATABASE = "pingu"
""" The default database to be used for the connection with
the mongo database """

BADGE_SIZE = 8
""" The size (in points) of the text to be used in the update
of the base badge image """

BADGE_FILL = "#666666"
""" The color to be used in the fill of the text for the update
operation in the badge """

DEFAULT_TIMEOUT = 60.0
""" The default timeout value to be used in between "ping"
requests, this values is only used as a fallback """

USER_TYPE = 1
""" The identifier (integer) to be used to represent an user
of type (normal) user """

ADMIN_TYPE = 2
""" The identifier (integer) to be used to represent an user
of type admin (administrator) """

USER_ACL = {
    USER_TYPE : (
        "index",
        "about",
        "servers.list",
        "servers.new",
        "servers.show",
        "servers.edit",
        "servers.delete",
        "log.list",
        "contacts.list",
        "contacts.new",
        "contacts.show",
        "contacts.edit",
        "contacts.delete",
        "accounts.show",
        "accounts.edit"
    ),
    ADMIN_TYPE : (
        "*",
    )
}
""" The map associating the user type with the corresponding
list (sequence) of access control tokens """

HEADERS = {
    "User-Agent" : "pingu/0.1.0",
    "X-Powered-By" : "hive-server/0.1.0"
}
""" The map of headers to be used as base for the pingu
http client to use """

app = flask.Flask(__name__)
quorum.load(
    app,
    redis_session = True,
    mongo_database = MONGO_DATABASE,
    name = "pingu.debug",
    models = models
)

navbar_h = None

# @TODO: improve this code
base_path = os.path.dirname(__file__)
heroku_conf = os.path.join(base_path, "heroku", "addon-manifest.json")
file = open(heroku_conf, "rb")
try: data = json.load(file)
finally: file.close()

# @TODO: improve this code, put this into
# a different place
api = data.get("api", {})
username_h = data.get("id", None)
password_h = api.get("password", None)
salt_h = api.get("sso_salt", None)

quorum.config_g["salt_h"] = salt_h

def create_servers_h(heroku_id, account, sleep_time = 3.0):
    # sleeps for a while so that no collision with the remote
    # server occurs (the application must be registered already)
    time.sleep(sleep_time)

    # retrieves the current instance id to be used
    # from the account structure provided, then encodes
    # the provided heroku id into url encode
    instance_id = account.instance_id
    heroku_id_e = urllib.quote(heroku_id)

    # creates the complete url string from the username,
    # password and heroku id to be used and the opens the
    # url reading its data
    url = "https://%s:%s@api.heroku.com/vendor/apps/%s" % (username_h, password_h, heroku_id_e)
    try:
        remote = urllib.urlopen(url)
        try: data = remote.read()
        finally: remote.close()
    except:
        data = "{}"

    # loads the json structure from the data and obtains the
    # owner email and the various domains contained in it
    object = json.loads(data)
    owner_email = object.get("owner_email", "")
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
        task = (server, DEFAULT_TIMEOUT)

        # saves the server instance and schedules the task, this
        # should ensure coherence in the internal data structures
        _schedule_task(task)

        # adds the servers structure to the list of servers that
        # have been created
        servers.append(server)

    # returns the complete set of servers creates to the
    # caller method
    return servers

def get_navbar_h():
    global navbar_h
    if navbar_h: return navbar_h
    server = urllib.urlopen("http://nav.heroku.com/v1/providers/header")
    try: data = server.read()
    finally: server.close()
    navbar_h = data
    return navbar_h

@app.context_processor
def utility_processor():
    return dict(acl = quorum.check_login)

@app.route("/heroku/resources", methods = ("POST",))
@quorum.ensure_auth(username_h, password_h, json = True)
def provision():
    # retrieves the complete set of data from the request
    # and then unpacks it into the expected attributes
    object = quorum.get_object()
    heroku_id = object["heroku_id"]
    plan = object["plan"]

    # creates the heroku account with the unpacked values from the
    # provided message
    account = models.Account.create_heroku(heroku_id, plan = plan)

    # schedules the execution of the server creation for
    # the current provision, this will be deferred so that
    # the call is only made after provision is complete
    quorum.run_background(
        create_servers_h,
        (heroku_id, account)
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
    object = quorum.get_object()
    plan = object["plan"]

    account = models.Account.get(username = id)
    account.plan = plan
    account.save()

    return "ok"

@app.route("/sso/login", methods = ("POST",))
def sso_login():
    # retrieves the various parameters provided by the
    # caller post operation to be used in the construction
    # of the response and security validations
    object = quorum.get_object()
    id = object.get("id", None)
    timestamp = object.get("timestamp", None)
    token = object.get("token", None)
    nav_data = object.get("nav-data", None)

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
    flask.session["acl"] = quorum.check_login

    # makes the current session permanent this will allow
    # the session to persist along multiple browser initialization
    flask.session.permanent = True

    # creates a new redirect request and uses it to create
    # the response object that is set with the cookie value
    # to be used by heroku navigation bar
    redirect = flask.redirect(
        flask.url_for("list_servers")
    )
    response = app.make_response(redirect)
    response.set_cookie("heroku-nav-data", value = nav_data)
    return response

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
    object = quorum.get_object()
    username = object.get("username", None)
    password = object.get("password", None)
    try: account = models.Account.login(username, password)
    except quorum.OperationalError, error:
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
    flask.session["acl"] = quorum.check_login

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

@app.route("/about", methods = ("GET",))
@quorum.ensure("about")
def about():
    return flask.render_template(
        "about.html.tpl",
        link = "about"
    )

@app.route("/accounts", methods = ("GET",))
@quorum.ensure("accounts.list")
def list_accounts():
    accounts = _get_accounts()
    return flask.render_template(
        "account_list.html.tpl",
        link = "accounts",
        sub_link = "list",
        accounts = accounts
    )

@app.route("/accounts.json", methods = ("GET",))
@quorum.ensure("accounts.list", json = True)
def list_accounts_json():
    start_record = int(flask.request.args.get("start_record", 0))
    number_records = int(flask.request.args.get("number_records", 6))
    accounts = _get_accounts(start = start_record, count = number_records)
    return flask.Response(
        quorum.dumps_mongo(accounts),
        mimetype = "application/json"
    )

@app.route("/accounts/new", methods = ("GET",))
def new_account():
    return flask.render_template(
        "account_new.html.tpl",
        link = "accounts",
        sub_link = "create",
        account = {},
        errors = {}
    )

@app.route("/accounts", methods = ("POST",))
def create_account():
    # creates the new account, using the provided arguments and
    # then saves it into the data source, all the validations
    # should be ran upon the save operation
    account = models.Account.new()
    try: account.save()
    except quorum.ValidationError, error:
        return flask.render_template(
            "account_new.html.tpl",
            link = "accounts",
            sub_link = "create",
            account = error.model,
            errors = error.errors
        )

    # redirects the user to the pending page, indicating that
    # the account is not yet activated and is pending the email
    # confirmation action
    return flask.redirect(
        flask.url_for("pending", username = account.username)
    )

@app.route("/accounts.json", methods = ("POST",))
@quorum.errors_json
def create_account_json():
    # creates the new account, using the provided arguments and
    # then saves it into the data source, all the validations
    # should be ran upon the save operation
    account = models.Account.new()
    account.save()

    return flask.Response(
        account.dumps(),
        mimetype = "application/json"
    )

@app.route("/accounts/<username>", methods = ("GET",))
@quorum.ensure("accounts.show")
def show_account(username):
    account = models.Account.get(username = username)
    return flask.render_template(
        "account_show.html.tpl",
        link = "accounts",
        sub_link = "info",
        account = account
    )

@app.route("/accounts/<username>/edit", methods = ("GET",))
@quorum.ensure("accounts.edit")
def edit_account(username):
    account = models.Account.get(username = username)
    return flask.render_template(
        "account_edit.html.tpl",
        link = "accounts",
        sub_link = "edit",
        account = account,
        errors = {}
    )

@app.route("/accounts/<username>/edit", methods = ("POST",))
@quorum.ensure("accounts.edit")
def update_account(username):
    # finds the current and account and applies the provided
    # arguments and then saves it into the data source,
    # all the validations should be ran upon the save operation
    account = models.Account.get(username = username)
    account.apply()
    try: account.save()
    except quorum.ValidationError, error:
        return flask.render_template(
            "account_edit.html.tpl",
            link = "accounts",
            sub_link = "edit",
            account = error.model,
            errors = error.errors
        )

    # redirects the user to the show page of the account that
    # was just updated
    return flask.redirect(
        flask.url_for("show_account", username = username)
    )

@app.route("/accounts/<username>/delete", methods = ("GET", "POST"))
@quorum.ensure("accounts.delete")
def delete_account(username):
    _delete_account(username)
    return flask.redirect(
        flask.url_for("list_accounts")
    )

@app.route("/servers", methods = ("GET",))
@quorum.ensure("servers.list")
def list_servers():
    servers = models.Server.find_i()
    return flask.render_template(
        "server_list.html.tpl",
        link = "servers",
        sub_link = "list",
        servers = servers
    )

@app.route("/servers/new", methods = ("GET",))
@quorum.ensure("servers.new")
def new_server():
    return flask.render_template(
        "server_new.html.tpl",
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
    except quorum.ValidationError, error:
        return flask.render_template(
            "server_new.html.tpl",
            link = "servers",
            sub_link = "create",
            server = error.model,
            errors = error.errors
        )

    # creates a task for the server that has just been created
    # this tuple is going to be used by the scheduling thread
    # @TODO: PUT THIS INTO DE POST_SAVE method
    task = (server, DEFAULT_TIMEOUT)

    # saves the server instance and schedules the task, this
    # should ensure coherence in the internal data structures
    # @TODO: put this as a static method under task model
    _schedule_task(task)

    # redirects the user to the show page of the server that
    # was just created
    return flask.redirect(
        flask.url_for("show_server", name = server.name)
    )

@app.route("/servers/<name>", methods = ("GET",))
@quorum.ensure("servers.show")
def show_server(name):
    server = models.Server.get(name = name)
    return flask.render_template(
        "server_show.html.tpl",
        link = "servers",
        sub_link = "info",
        server = server
    )

@app.route("/servers/<name>/edit", methods = ("GET",))
@quorum.ensure("servers.edit")
def edit_server(name):
    server = _get_server(name)
    return flask.render_template(
        "server_edit.html.tpl",
        link = "servers",
        sub_link = "edit",
        server = server,
        errors = {}
    )

@app.route("/servers/<name>/edit", methods = ("POST",))
@quorum.ensure("servers.edit")
def update_server(name):
    # runs the validation process on the various arguments
    # provided to the server
    errors, server = quorum.validate("server")
    if errors:
        return flask.render_template(
            "server_edit.html.tpl",
            link = "servers",
            sub_link = "edit",
            server = server,
            errors = errors
        )

    # retrieves all the parameters from the request to be
    # handled then validated the required ones
    url = flask.request.form.get("url", None)
    description = flask.request.form.get("description", None)

    # populates the structure to be used as the server description
    # using the values provided as parameters
    server = _get_server(name, build = False)
    server["url"] = url
    server["description"] = description

    # saves the server instance, this should ensure coherence
    # in the internal data structures
    _save_server(server)

    # redirects the user to the show page of the server that
    # was just created
    return flask.redirect(
        flask.url_for("show_server", name = name)
    )

@app.route("/servers/<name>/delete", methods = ("GET", "POST"))
@quorum.ensure("servers.delete")
def delete_server(name):
    server = models.Server.get(name = name)
    server.delete()
    return flask.redirect(
        flask.url_for("list_servers")
    )

@app.route("/servers/<name>/log", methods = ("GET",))
@quorum.ensure("log.list")
def list_log(name):
    server = models.Server.get(name = name)
    return flask.render_template(
        "server_log.html.tpl",
        link = "servers",
        sub_link = "log",
        server = server
    )

@app.route("/servers/<name>/log.json", methods = ("GET",))
@quorum.ensure("log.list", json = True)
def list_log_json(name):
    object = quorum.get_object(alias = True, find = True)
    log = models.Log.find(map = True, name = name, **object)
    return flask.Response(
        quorum.dumps_mongo(log),
        mimetype = "application/json"
    )

@app.route("/contacts", methods = ("GET",))
@quorum.ensure("contacts.list")
def list_contacts():
    contacts = _get_contacts()
    return flask.render_template(
        "contact_list.html.tpl",
        link = "contacts",
        sub_link = "list",
        contacts = contacts
    )

@app.route("/contacts/new", methods = ("GET",))
@quorum.ensure("contacts.new")
def new_contact():
    return flask.render_template(
        "contact_new.html.tpl",
        link = "contacts",
        sub_link = "create",
        contact = {},
        errors = {}
    )

@app.route("/contacts", methods = ("POST",))
@quorum.ensure("contacts.new")
def create_contact():
    # runs the validation process on the various arguments
    # provided to the account
    errors, contact = quorum.validate("contact_new")
    if errors:
        return flask.render_template(
            "contact_new.html.tpl",
            link = "contacts",
            sub_link = "create",
            contact = contact,
            errors = errors
        )

    # retrieves all the parameters from the request to be
    # handled then validated the required ones
    name = flask.request.form.get("name", None)
    email = flask.request.form.get("email", None)
    phone = flask.request.form.get("phone", None)
    xmpp = flask.request.form.get("xmpp", None)
    twitter = flask.request.form.get("twitter", None)
    facebook = flask.request.form.get("facebook", None)

    # generates a new identifier for the contact to be created
    # this will be used to access the contact
    id = str(uuid.uuid4())

    # creates the structure to be used as the server description
    # using the values provided as parameters
    contact = {
        "enabled" : True,
        "instance_id" : flask.session["instance_id"],
        "id" : id,
        "name" : name,
        "email" : email,
        "phone" : phone,
        "xmpp" : xmpp,
        "twitter" : twitter,
        "facebook" : facebook
    }

    # saves the contact instance into the data source, ensures
    # that the account is ready for processing
    _save_contact(contact)

    # redirects the user to the show page of the contact that
    # was just created
    return flask.redirect(
        flask.url_for("show_contact", id = id)
    )

@app.route("/contacts/<id>", methods = ("GET",))
@quorum.ensure("contacts.show")
def show_contact(id):
    contact = _get_contact(id)
    return flask.render_template(
        "contact_show.html.tpl",
        link = "contacts",
        sub_link = "info",
        contact = contact
    )

@app.route("/contacts/<id>/edit", methods = ("GET",))
@quorum.ensure("contacts.edit")
def edit_contact(id):
    contact = _get_contact(id)
    return flask.render_template(
        "contact_edit.html.tpl",
        link = "contacts",
        sub_link = "edit",
        contact = contact,
        errors = {}
    )

@app.route("/contacts/<id>/edit", methods = ("POST",))
@quorum.ensure("contacts.edit")
def update_contact(id):
    # runs the validation process on the various arguments
    # provided to the server
    errors, contact = quorum.validate("contact")
    if errors:
        return flask.render_template(
            "contact_edit.html.tpl",
            link = "contacts",
            sub_link = "edit",
            contact = contact,
            errors = errors
        )

    # retrieves all the parameters from the request to be
    # handled then validated the required ones
    name = flask.request.form.get("name", None)
    email = flask.request.form.get("email", None)
    phone = flask.request.form.get("phone", None)
    xmpp = flask.request.form.get("xmpp", None)
    twitter = flask.request.form.get("twitter", None)
    facebook = flask.request.form.get("facebook", None)

    # creates the structure to be used as the contact description
    # using the values provided as parameters
    contact = _get_contact(id, build = False)
    contact["name"] = name
    contact["email"] = email
    contact["phone"] = phone
    contact["xmpp"] = xmpp
    contact["twitter"] = twitter
    contact["facebook"] = facebook

    # saves the contact instance into the data source, ensures
    # that the account is ready for processing
    _save_contact(contact)

    # redirects the user to the show page of the contact that
    # was just created
    return flask.redirect(
        flask.url_for("show_contact", id = id)
    )

@app.route("/contacts/<id>/delete", methods = ("GET", "POST"))
@quorum.ensure("contacts.delete")
def delete_contact(id):
    _delete_contact(id)
    return flask.redirect(
        flask.url_for("list_contacts")
    )

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
    # @TODO: update this text value with a dynamically
    # generated value
    TEXT = "51,36%"

    # creates both the complete file path for the badge
    # file and the file path to the font file to be used
    # in the generation of the badge
    badge_path = os.path.join(base_path, "static/images/site/badge-uptime.png")
    font_path = os.path.join(base_path, "static/fonts/pixel_arial.ttf")

    # creates the font object to be used in the "writing"
    # for the file and retrieves the size of the text for
    # the create font
    font = PIL.ImageFont.truetype(font_path, BADGE_SIZE)
    width, height = font.getsize(TEXT)

    # opens the badge image file and retrieves the png based
    # information tuple and the size of that image
    image = PIL.Image.open(badge_path, "r")
    png_info = image.info
    image_width, image_height = image.size

    # calculates the horizontal and vertical text position based
    # on the current image and text dimensions
    x = image_width - width - 3
    y = (image_height / 2) - (height / 2)

    # creates the draw context for the current image, in order to
    # be able to "draw" the text in it
    draw = PIL.ImageDraw.Draw(image)
    draw.text((x, y), TEXT, font = font, fill = BADGE_FILL)

    # creates the buffer for the writing of the "final" image file,
    # then writes its contents and reads the complete set of data
    buffer = cStringIO.StringIO()
    try:
        image.save(buffer, "png", **png_info)
        buffer.seek(0)
        data = buffer.read()
    finally:
        buffer.close()

    # returns the "binary" response as a png based image (the "just
    # generated badge image)
    return flask.Response(
        data,
        mimetype = "image/png"
    )

def _get_accounts(start = 0, count = 6):
    pymongo = quorum.mongodb.pymongo
    db = quorum.get_mongo_db()
    accounts = db.accounts.find(
        {"enabled" : True},
        skip = start,
        limit = count,
        sort = [("last_login", pymongo.DESCENDING)]
    )
    accounts = [_build_account(account) for account in accounts]
    return accounts

def _get_account(username, build = True, raise_e = True):
    db = quorum.get_mongo_db()
    account = db.accounts.find_one({
        "enabled" : True,
        "username" : username
    })
    if not account and raise_e: raise RuntimeError("Account not found")
    build and _build_account(account)
    return account

def _get_all_account(username, build = True, raise_e = True):
    db = quorum.get_mongo_db()
    account = db.accounts.find_one({
        "username" : username
    })
    if not account and raise_e: raise RuntimeError("Account not found")
    build and _build_account(account)
    return account

def _get_account_confirmation(confirmation):
    db = quorum.get_mongo_db()
    account = db.accounts.find_one({
        "confirmation" : confirmation
    })
    return account

def _save_account(account):
    db = quorum.get_mongo_db()
    db.accounts.save(account)
    return account

def _delete_account(username):
    db = quorum.get_mongo_db()
    account = db.accounts.find_one({"username" : username})
    account["enabled"] = False
    db.accounts.save(account)
    return account

def _remove_account(username):
    db = quorum.get_mongo_db()
    account = db.accounts.find_one({"username" : username})
    instance_id = account["instance_id"]
    db.contacts.remove({"instance_id" : instance_id})
    db.log.remove({"instance_id" : instance_id})
    db.servers.remove({"instance_id" : instance_id})
    db.accounts.remove({"instance_id" : instance_id})

def _confirm_account(account):
    username = account.get("username", None)
    email = account.get("email", None)

    parameters = {
        "subject" : "Welcome to Pingu, please confirm you email",
        "sender" : "Pingu Mailer <mailer@pinguapp.com>",
        "receivers" : ["%s <%s>" % (username, email)],
        "plain" : "email/confirm.txt.tpl",
        "rich" : "email/confirm.html.tpl",
        "context" : {
            "account" : account
        }
    }
    thread.start_new_thread(_send_email, (), parameters)

def _get_servers():
    db = quorum.get_mongo_db()
    servers = db.servers.find({
        "enabled" : True,
        "instance_id" : flask.session["instance_id"]
    })
    servers = [_build_server(server) for server in servers]
    return servers

def _get_all_servers():
    db = quorum.get_mongo_db()
    servers = db.servers.find({
        "enabled" : True
    })
    servers = [_build_server(server) for server in servers]
    return servers

def _get_server(name, build = True, raise_e = True):
    db = quorum.get_mongo_db()
    server = db.servers.find_one({
        "instance_id" : flask.session["instance_id"],
        "name" : name
    })
    if not server and raise_e: raise RuntimeError("Server not found")
    build and _build_server(server)
    return server

def _save_server(server):
    db = quorum.get_mongo_db()
    db.servers.save(server)
    return server

def _delete_server(name):
    db = quorum.get_mongo_db()
    server = db.servers.find_one({"name" : name})
    server["enabled"] = False
    db.servers.save(server)
    return server

def _get_log(name, start = 0, count = 6):
    pymongo = quorum.mongodb.pymongo
    db = quorum.get_mongo_db()
    log = db.log.find(
        {
            "instance_id" : flask.session["instance_id"],
            "name" : name
        },
        skip = start,
        limit = count,
        sort = [("timestamp", pymongo.DESCENDING)]
    )
    log = [_build_log(_log) for _log in log]
    return log

def _get_contacts():
    db = quorum.get_mongo_db()
    contacts = db.contacts.find({
        "enabled" : True,
        "instance_id" : flask.session["instance_id"]
    })
    contacts = [_build_contact(contact) for contact in contacts]
    return contacts

def _get_contact(id, build = True, raise_e = True):
    db = quorum.get_mongo_db()
    contact = db.contacts.find_one({
        "instance_id" : flask.session["instance_id"],
        "id" : id
    })
    if not contact and raise_e: raise RuntimeError("Contact not found")
    build and _build_contact(contact)
    return contact

def _save_contact(contact):
    db = quorum.get_mongo_db()
    db.contacts.save(contact)
    return contact

def _delete_contact(id):
    db = quorum.get_mongo_db()
    contact = db.contacts.find_one({"id" : id})
    contact["enabled"] = False
    db.contacts.save(contact)
    return contact

def _validate_account_new():
    return [
        quorum.not_null("username"),
        quorum.not_empty("username"),
        quorum.string_gt("username", 4),
        quorum.string_lt("username", 20),
        quorum.not_duplicate("username", "accounts"),

        quorum.validation.not_null("password"),
        quorum.validation.not_empty("password"),

        quorum.validation.not_null("password_confirm"),
        quorum.validation.not_empty("password_confirm"),

        quorum.not_null("email"),
        quorum.not_empty("email"),
        quorum.is_email("email"),
        quorum.not_duplicate("email", "accounts"),

        quorum.not_null("email_confirm"),
        quorum.not_empty("email_confirm"),

        quorum.not_null("plan"),
        quorum.not_empty("plan"),
        quorum.is_in("plan", ("basic", "advanced")),

        quorum.equals("password_confirm", "password"),
        quorum.equals("email_confirm", "email")
    ] + _validate_account()

def _validate_account():
    return []

def _validate_server_new():
    return [
        quorum.not_null("name"),
        quorum.not_empty("name"),
        quorum.not_duplicate("name", "servers"),
    ] + _validate_server()

def _validate_server():
    return [
        quorum.not_null("url"),
        quorum.not_empty("url"),
        quorum.is_url("url"),

        quorum.not_null("description"),
        quorum.not_empty("description")
    ]

def _validate_contact_new():
    return [] + _validate_contact()

def _validate_contact():
    return [
        quorum.not_null("name"),
        quorum.not_empty("name"),

        quorum.not_null("email"),
        quorum.not_empty("email"),
        quorum.is_email("email")
    ]

def _build_account(account):
    enabled = account.get("enabled", False)
    email = account.get("email", None)
    last_login = account.get("last_login", None)
    last_login_date = last_login and datetime.datetime.utcfromtimestamp(last_login)
    last_login_string = last_login_date and last_login_date.strftime("%d/%m/%Y %H:%M:%S")
    account["enabled_l"] = enabled and "enabled" or "disabled"
    account["email_s"] = email and email.replace("@", " at ").replace(".", " dot ")
    account["last_login_l"] = last_login_string
    del account["password"]
    return account

def _build_server(server):
    up = server.get("up", None)
    server["up_l"] = up == True and "up" or up == False and "down" or "unknwon"
    return server

def _build_log(log):
    up = log.get("up", None)
    timestamp = log.get("timestamp", None)
    date = datetime.datetime.utcfromtimestamp(timestamp)
    date_string = date.strftime("%d/%m/%Y %H:%M:%S")
    log["up_l"] = up == True and "up" or up == False and "down" or "unknwon"
    log["date_l"] = date_string
    return log

def _build_contact(contact):
    email = contact.get("email", None)
    contact["email_md5"] = email and hashlib.md5(email).hexdigest()
    return contact

def _send_email(subject = "", sender = "", receivers = [], plain = None, rich = None, context = {}):
    plain_data = plain and _render(plain, **context)
    html_data = rich and _render(rich, **context)

    message = email.mime.multipart.MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ", ".join(receivers)

    # creates both the plain text and the rich text (html) objects
    # from the provided data and then attached them to the message
    # (multipart alternative) that is the base structure
    plain = plain_data and email.mime.text.MIMEText(plain_data, "plain")
    html = html_data and email.mime.text.MIMEText(html_data, "html")
    plain and message.attach(plain)
    html and message.attach(html)

    # creates the connection with the smtp server and starts the tls
    # connection to send the created email message
    server = smtplib.SMTP(config.SMTP_HOST)
    try:
        server.starttls()
        server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        server.sendmail(sender, receivers, message.as_string())
    finally:
        server.quit()

def _ping(server, timeout = 1.0):
    # retrieves the name of the server that is goin to be
    # targeted by the "ping" operation
    name = server["name"]

    # retrieves the server again to ensure that the data
    # is correct in it
    db = quorum.get_mongo_db()
    server = db.servers.find_one({"name" : name})

    # retrieves the various attribute values from the server
    # that are going to be used in the method
    instance_id = server["instance_id"]
    name = server["name"]
    url = server["url"]
    method = server.get("method", "GET")

    # parses the provided url values, retrieving the various
    # components of it to be used in the ping operation
    url_s = urlparse.urlparse(url)
    scheme = url_s.scheme
    hostname = url_s.hostname
    port = url_s.port
    path = url_s.path

    # retrieves the connection class to be used according
    # to the scheme defined in the url
    connection_c = scheme == "https" and httplib.HTTPSConnection or httplib.HTTPConnection

    # retrieves the timestamp for the start of the connection
    # to the remote host and then creates a new connection to
    # the remote host to proceed with the "ping" operation
    start_time = time.time()
    connection = connection_c(hostname, port)
    try:
        connection.request(method, path, headers = HEADERS)
        response = connection.getresponse()
    except:
        response = None
    finally:
        connection.close()
    end_time = time.time()
    latency = int((end_time - start_time) * 1000.0)

    # retrieves both the status and the reason values
    # defaulting to "down" values in case the response
    # is not available
    status = response and response.status or 0
    reason = response and response.reason or "Down"

    # checks if the current status code is in the
    # correct range these are considered the "valid"
    # status codes for an up server
    up = (status / 100) in (2, 3)

    # prints a debug message about the ping operation
    # with the complete diagnostics information
    print "%s :: %s %s / %dms" % (url, status, reason, latency)

    # inserts the log document into the database so that
    # the information is registered
    db.log.insert({
        "enabled" : True,
        "instance_id" : instance_id,
        "name" : name,
        "url" : url,
        "up" : up,
        "status" : status,
        "reason" : reason,
        "latency" : latency,
        "timestamp" : start_time
    })

    change_down = not server.get("up", True) == up and not up
    change_up = not server.get("up", True) == up and up
    server["up"] = up
    server["latency"] = latency
    server["timestamp"] = start_time
    db.servers.save(server)

    # in case there's a change from server state up to down, or
    # down to up (reversed) must trigger the proper event so
    # that the user is notified about the change
    if change_down: _event_down(server)
    if change_up: _event_up(server)

    # retrieves the value for the enabled flag of the server
    # in case the values is not enable no re-scheduling is done
    enabled = server.get("enabled", False)

    # retrieves the current time and uses that value to
    # re-insert a new task into the execution thread, this
    # is considered the re-schedule operation
    current_time = time.time()
    enabled and execution_thread.insert_work(
        current_time + timeout,
        _ping_m(server, timeout = timeout)
    )

def _ping_m(server, timeout = 1.0):
    def _pingu(): _ping(server, timeout = timeout)
    return _pingu

def _event_down(server):
    name = server.get("name", None)
    parameters = {
        "subject" : "Your server %s, is currently down" % name,
        "sender" : "Pingu Mailer <mailer@pinguapp.com>",
        "receivers" : ["João Magalhães <joamag@hive.pt>"],
        "plain" : "email/down.txt.tpl",
        "rich" : "email/down.html.tpl",
        "context" : {
            "server" : server
        }
    }
    thread.start_new_thread(_send_email, (), parameters)

def _event_up(server):
    name = server.get("name", None)
    parameters = {
        "subject" : "Your server %s, is back online" % name,
        "sender" : "Pingu Mailer <mailer@pinguapp.com>",
        "receivers" : ["João Magalhães <joamag@hive.pt>"],
        "plain" : "email/up.txt.tpl",
        "rich" : "email/up.html.tpl",
        "context" : {
            "server" : server
        }
    }
    thread.start_new_thread(_send_email, (), parameters)

def _render(template_name, **context):
    template = app.jinja_env.get_or_select_template(template_name)
    return flask.templating._render(template, context, app)

def _ensure_db():
    db = quorum.get_mongo_db()

    db.accounts.ensure_index("enabled")
    db.accounts.ensure_index("instance_id")
    db.accounts.ensure_index("username")
    db.accounts.ensure_index("api_key")
    db.accounts.ensure_index("confirmation")
    db.accounts.ensure_index("email")
    db.accounts.ensure_index("twitter")
    db.accounts.ensure_index("facebook")
    db.accounts.ensure_index("last_login")

    db.servers.ensure_index("enabled")
    db.servers.ensure_index("instance_id")
    db.servers.ensure_index("name")
    db.servers.ensure_index("url")
    db.servers.ensure_index("up")
    db.servers.ensure_index("latency")
    db.servers.ensure_index("timestamp")

    db.log.ensure_index("instance_id")
    db.log.ensure_index("name")
    db.log.ensure_index("up")
    db.log.ensure_index("timestamp")

    db.contacts.ensure_index("enabled")
    db.contacts.ensure_index("instance_id")
    db.contacts.ensure_index("name")
    db.contacts.ensure_index("email")
    db.contacts.ensure_index("phone")

def _setup_db():
    db = quorum.get_mongo_db()
    root = db.accounts.find_one({
        "username" : "root",
        "type" : ADMIN_TYPE
    })
    if root: return

    # encodes the provided password into an sha1 hash appending
    # the salt value to it before the encoding
    password_sha1 = hashlib.sha1("root" + PASSWORD_SALT).hexdigest()

    # creates the structure to be used as the server description
    # using the values provided as parameters
    account = {
        "enabled" : True,
        "instance_id" : str(uuid.uuid4()),
        "username" : "root",
        "password" : password_sha1,
        "plan" : "full",
        "email" : "root@pinguapp.com",
        "login_count" : 0,
        "last_login" : None,
        "type" : ADMIN_TYPE,
        "tokens" : USER_ACL.get(ADMIN_TYPE, ())
    }

    # saves the account instance into the data source, ensures
    # that the account is ready for login
    _save_account(account)

def _get_tasks():
    tasks = []
    servers = _get_all_servers()

    for server in servers:
        timeout = server.get("timeout", DEFAULT_TIMEOUT)
        tasks.append((
            server,
            timeout
        ))

    return tasks + list(TASKS)

def _schedule_tasks():
    # retrieves the current time and then iterates over
    # all the tasks to insert them into the execution thread
    tasks = _get_tasks()
    for task in tasks: _schedule_task(task)

def _schedule_task(task):
    current_time = time.time()
    server, timeout = task
    execution_thread.insert_work(
        current_time,
        _ping_m(server, timeout = timeout)
    )

def load():
    # sets the global wide application settings and
    # configures the application object according to
    # this settings
    debug = os.environ.get("DEBUG", False) and True or False
    smtp_host = os.environ.get("SMTP_HOST", "localhost")
    smtp_user = os.environ.get("SMTP_USER", None)
    smtp_password = os.environ.get("SMTP_PASSWORD", None)
    config.SMTP_HOST = smtp_host
    config.SMTP_USER = smtp_user
    config.SMTP_PASSWORD = smtp_password
    app.debug = debug
    app.secret_key = SECRET_KEY

def run_waitress():
    import waitress

    # sets the debug control in the application
    # then checks the current environment variable
    # for the target port for execution (external)
    # and then start running it (continuous loop)
    debug = os.environ.get("DEBUG", False) and True or False
    smtp_host = os.environ.get("SMTP_HOST", "localhost")
    smtp_user = os.environ.get("SMTP_USER", None)
    smtp_password = os.environ.get("SMTP_PASSWORD", None)
    port = int(os.environ.get("PORT", 5000))
    config.SMTP_HOST = smtp_host
    config.SMTP_USER = smtp_user
    config.SMTP_PASSWORD = smtp_password
    app.debug = debug
    app.secret_key = SECRET_KEY
    waitress.serve(app, host = "0.0.0.0", port = port)

def run():
    # sets the debug control in the application
    # then checks the current environment variable
    # for the target port for execution (external)
    # and then start running it (continuous loop)
    debug = os.environ.get("DEBUG", False) and True or False
    reloader = os.environ.get("RELOADER", False) and True or False
    smtp_host = os.environ.get("SMTP_HOST", "localhost")
    smtp_user = os.environ.get("SMTP_USER", None)
    smtp_password = os.environ.get("SMTP_PASSWORD", None)
    port = int(os.environ.get("PORT", 5000))
    config.SMTP_HOST = smtp_host
    config.SMTP_USER = smtp_user
    config.SMTP_PASSWORD = smtp_password
    app.debug = debug
    app.secret_key = SECRET_KEY
    app.run(
        use_debugger = debug,
        debug = debug,
        use_reloader = reloader,
        host = "0.0.0.0",
        port = port
    )

@atexit.register
def stop_thread():
    # stop the execution thread so that it's possible to
    # the process to return the calling
    execution_thread.stop()

# creates the thread that it's going to be used to
# execute the various background tasks and starts
# it, providing the mechanism for execution
execution_thread = quorum.execution.ExecutionThread()
execution_thread.start()

# ensures the various requirements for the database
# so that it becomes ready for usage
_setup_db()
_ensure_db()

# schedules the various tasks currently registered in
# the system internal structures
_schedule_tasks()

if __name__ == "__main__": run()
else: load()
