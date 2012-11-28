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
import hashlib
import httplib
import smtplib
import datetime
import urlparse

import email.mime.multipart
import email.mime.text

import config
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

MONGO_URL = "mongodb://localhost:27017"
""" The default url to be used for the connection with
the mongo database """

MONGO_DATABASE = "pingu"
""" The default database to be used for the connection with
the mongo database """

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
#app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(365)
#app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
#app.config["MAX_CONTENT_LENGTH"] = 1024 ** 3

mongo_url = os.getenv("MONGOHQ_URL", MONGO_URL)
quorum.mongo.url = mongo_url
quorum.mongo.database = MONGO_DATABASE


@app.route("/heroku/resources", methods = ("POST",))
def provision():
    return json.dumps({
        "id" : str(uuid.uuid4())
    })

@app.route("/heroku/resources/<id>", methods = ("PUT",))
def plan_change(id):
    return "ok"

@app.route("/heroku/resources/<id>", methods = ("PUT",))
def deprovision(id):
    return "ok"

@app.route("/heroku/resources/<id>", methods = ("GET",))
def sso_resources(id):
    return flask.redirect(
        flask.url_for("sso")
    )

@app.route("/sso/login", methods = ("POST",))
def sso_login(id):
    return flask.redirect(
        flask.url_for("sso_redirect")
    )

@app.route("/sso/redirect", methods = ("GET",))
def sso_redirect():
    return "ok"

#@app.route("/heroku/resources/<id>", methods = ("PUT",))
#def deprovision(id):
#    return "ok"
#
#//GET SSO
#app.get('/heroku/resources/:id', sso_auth, function(request, response) {
#  response.redirect("/")
#})
#
#//POST SSO
#app.post('/sso/login', express.bodyParser(), sso_auth, function(request, response){
#  response.redirect("/")
#})

#===============================================================================
# app.put('/heroku/resources/:id', express.bodyParser(), basic_auth, function(request, response) {
#  console.log(request.body)
#  console.log(request.params)
#  var resource =  get_resource(request.params.id)
#  if(!resource){
#    response.send("Not found", 404);
#    return;
#  }
#  resource.plan = request.body.plan
#  response.send("ok")
# })
#===============================================================================






@app.route("/", methods = ("GET",))
@app.route("/index", methods = ("GET",))
@quorum.extras.ensure("index")
def index():
    return flask.render_template(
        "index.html.tpl",
        link = "home"
    )

@app.route("/pending", methods = ("GET",))
def pending():
    #@TODO: must implement this
    return flask.render_template(
        "pending.html.tpl"
    )

@app.route("/resend", methods = ("GET",))
def resend():
    #@TODO: must implement this
    return flask.render_template(
        "pending.html.tpl"
    )

@app.route("/signin", methods = ("GET",))
def signin():
    return flask.render_template(
        "signin.html.tpl"
    )

@app.route("/signin", methods = ("POST",))
def login():
    # retrieves both the username and the password from
    # the flask request form, these are the values that
    # are going to be used in the username validation
    username = flask.request.form.get("username", None)
    password = flask.request.form.get("password", None)

    # in case any of the mandatory arguments is not provided
    # an error is set in the current page
    if not username or not password:
        return flask.render_template(
            "signin.html.tpl",
            username = username,
            error = "Both username and password must be provided"
        )

    # retrieves the structure containing the information
    # on the currently available users and unpacks the
    # various attributes from it (defaulting to base values)
    account = _get_account(username, build = False, raise_e = False) or {}
    _username = account.get("username", None)
    _password = account.get("password", None)

    # encodes the provided password into an sha1 hash appending
    # the salt value to it before the encoding
    password_sha1 = hashlib.sha1(password + PASSWORD_SALT).hexdigest()

    # checks that both the account structure and the password values
    # are present and that the password matched, if one of these
    # values fails the login process fails and the user is redirected
    # to the signin page with an error string
    if not account or not _password or not password_sha1 == _password:
        return flask.render_template(
            "signin.html.tpl",
            username = username,
            error = "Invalid username and/or password"
        )

    # sets the login count and last login values in the account as the
    # current time and then saves it in the data store
    login_count = account.get("login_count", 0)
    account["login_count"] = login_count + 1
    account["last_login"] = time.time()
    _save_account(account)

    # retrieves the tokens and instance id from the user to set
    # them in the current session
    tokens = account.get("tokens", ())
    instance_id = account.get("instance_id", None)

    # updates the current user (name) in session with
    # the username that has just be accepted in the login
    flask.session["username"] = username
    flask.session["tokens"] = tokens
    flask.session["instance_id"] = instance_id

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
    if "cameras" in flask.session: del flask.session["cameras"]

    return flask.redirect(
        flask.url_for("signin")
    )

@app.route("/about", methods = ("GET",))
@quorum.extras.ensure("about")
def about():
    return flask.render_template(
        "about.html.tpl",
        link = "about"
    )

@app.route("/accounts", methods = ("GET",))
@quorum.extras.ensure("accounts.list")
def list_accounts():
    accounts = _get_accounts()
    return flask.render_template(
        "account_list.html.tpl",
        link = "accounts",
        accounts = accounts
    )

@app.route("/accounts.json", methods = ("GET",))
@quorum.extras.ensure("accounts.list", json = True)
def accounts_json():
    start_record = int(flask.request.args.get("start_record", 0))
    number_records = int(flask.request.args.get("number_records", 6))
    accounts = _get_accounts(start = start_record, count = number_records)
    return flask.Response(
        quorum.mongo.dumps(accounts),
        mimetype = "application/json"
    )

@app.route("/accounts/new", methods = ("GET",))
def new_account():
    return flask.render_template(
        "account_new.html.tpl",
        link = "new_account",
        account = {},
        errors = {}
    )

@app.route("/accounts", methods = ("POST",))
def create_account():
    # runs the validation process on the various arguments
    # provided to the account
    errors, account = quorum.validate("account_new")
    if errors:
        return flask.render_template(
            "account_new.html.tpl",
            link = "new_account",
            account = account,
            errors = errors
        )

    # retrieves all the parameters from the request to be
    # handled then validated the required ones
    _username = flask.request.form.get("username", None)
    password = flask.request.form.get("password", None)
    email = flask.request.form.get("email", None)

    # "encrypts" the password into the target format defined
    # by the salt and the sha1 hash function
    password_sha1 = hashlib.sha1(password + PASSWORD_SALT).hexdigest()

    # creates the structure to be used as the server description
    # using the values provided as parameters
    account = {
        "enabled" : False,
        "instance_id" : str(uuid.uuid4()),
        "username" : _username,
        "password" : password_sha1,
        "email" : email,
        "login_count" : 0,
        "last_login" : None,
        "type" : USER_TYPE,
        "tokens" : USER_ACL.get(USER_TYPE, ())
    }

    # saves the account instance into the data source, ensures
    # that the account is ready for login
    _save_account(account)

    # redirects the user to the show page of the account that
    # was just created
    return flask.redirect(
        flask.url_for("show_account", username = _username)
    )

@app.route("/accounts/<username>", methods = ("GET",))
@quorum.extras.ensure("accounts.show")
def show_account(username):
    account = _get_account(username)
    return flask.render_template(
        "account_show.html.tpl",
        link = "accounts",
        sub_link = "info",
        account = account
    )

@app.route("/accounts/<username>/edit", methods = ("GET",))
@quorum.extras.ensure("accounts.edit")
def edit_account(username):
    account = _get_account(username)
    return flask.render_template(
        "account_edit.html.tpl",
        link = "accounts",
        sub_link = "edit",
        account = account,
        errors = {}
    )

@app.route("/accounts/<username>/edit", methods = ("POST",))
@quorum.extras.ensure("accounts.edit")
def update_account(username):
    # runs the validation process on the various arguments
    # provided to the account
    errors, account = quorum.validate("account")
    if errors:
        return flask.render_template(
            "server_edit.html.tpl",
            link = "accounts",
            sub_link = "edit",
            account = account,
            errors = errors
        )

    # retrieves all the parameters from the request to be
    # handled then validated the required ones
    password = flask.request.form.get("password", None)
    phone = flask.request.form.get("phone", None)
    twitter = flask.request.form.get("twitter", None)
    facebook = flask.request.form.get("facebook", None)

    # "encrypts" the password into the target format defined
    # by the salt and the sha1 hash function
    password_sha1 = password and hashlib.sha1(password + PASSWORD_SALT).hexdigest()

    # populates the structure to be used as the server description
    # using the values provided as parameters
    account = _get_account(username, build = False)
    if password_sha1: account["password"] = password_sha1
    account["phone"] = phone
    account["twitter"] = twitter
    account["facebook"] = facebook

    # saves the account instance into the data source, ensures
    # that the account is ready for login
    _save_account(account)

    # redirects the user to the show page of the account that
    # was just created
    return flask.redirect(
        flask.url_for("show_account", username = username)
    )

@app.route("/accounts/<username>/delete", methods = ("GET", "POST"))
@quorum.extras.ensure("accounts.delete")
def delete_account(username):
    _delete_account(username)
    return flask.redirect(
        flask.url_for("list_accounts")
    )

@app.route("/servers", methods = ("GET",))
@quorum.extras.ensure("servers.list")
def list_servers():
    servers = _get_servers()
    return flask.render_template(
        "server_list.html.tpl",
        link = "servers",
        servers = servers
    )

@app.route("/servers/new", methods = ("GET",))
@quorum.extras.ensure("servers.new")
def new_server():
    return flask.render_template(
        "server_new.html.tpl",
        link = "new_server",
        server = {},
        errors = {}
    )

@app.route("/servers", methods = ("POST",))
@quorum.extras.ensure("servers.new")
def create_server():
    # runs the validation process on the various arguments
    # provided to the server
    errors, server = quorum.validate("server")
    if errors:
        return flask.render_template(
            "server_new.html.tpl",
            link = "new_server",
            server = server,
            errors = errors
        )

    # retrieves all the parameters from the request to be
    # handled then validated the required ones
    _name = flask.request.form.get("name", None)
    url = flask.request.form.get("url", None)
    description = flask.request.form.get("description", None)

    # creates the structure to be used as the server description
    # using the values provided as parameters
    server = {
        "enabled" : True,
        "instance_id" : flask.session["instance_id"],
        "name" : _name,
        "url" : url,
        "description" : description
    }

    # creates a task for the server that has just been created
    # this tuple is going to be used by the scheduling thread
    task = (server, 5.0)

    # saves the server instance and schedules the task, this
    # should ensure coherence in the internal data structures
    _save_server(server)
    _schedule_task(task)

    # redirects the user to the show page of the server that
    # was just created
    return flask.redirect(
        flask.url_for("show_server", name = _name)
    )

    return update_server()

@app.route("/servers/<name>", methods = ("GET",))
@quorum.extras.ensure("servers.show")
def show_server(name):
    server = _get_server(name)
    return flask.render_template(
        "server_show.html.tpl",
        link = "servers",
        sub_link = "info",
        server = server
    )

@app.route("/servers/<name>/edit", methods = ("GET",))
@quorum.extras.ensure("servers.edit")
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
@quorum.extras.ensure("servers.edit")
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
    server = _get_server(name)
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
@quorum.extras.ensure("servers.delete")
def delete_server(name):
    _delete_server(name)
    return flask.redirect(
        flask.url_for("list_servers")
    )

@app.route("/servers/<name>/log", methods = ("GET",))
@quorum.extras.ensure("log.list")
def list_log(name):
    server = _get_server(name)
    return flask.render_template(
        "server_log.html.tpl",
        link = "servers",
        sub_link = "log",
        server = server
    )

@app.route("/servers/<name>/log.json", methods = ("GET",))
@quorum.extras.ensure("log.list", json = True)
def list_log_json(name):
    start_record = int(flask.request.args.get("start_record", 0))
    number_records = int(flask.request.args.get("number_records", 6))
    log = _get_log(name, start = start_record, count = number_records)
    return flask.Response(
        quorum.mongo.dumps(log),
        mimetype = "application/json"
    )

def _get_accounts(start = 0, count = 6):
    pymongo = quorum.mongo.pymongo
    db = quorum.mongo.get_db()
    accounts = db.accounts.find(
        {"enabled" : True},
        skip = start,
        limit = count,
        sort = [("last_login", pymongo.DESCENDING)]
    )
    accounts = [_build_account(account) for account in accounts]
    return accounts

def _get_account(username, build = True, raise_e = True):
    db = quorum.mongo.get_db()
    account = db.accounts.find_one({"username" : username})
    if not account and raise_e: raise RuntimeError("Account not found")
    build and _build_account(account)
    return account

def _save_account(account):
    db = quorum.mongo.get_db()
    db.accounts.save(account)
    return account

def _delete_account(username):
    db = quorum.mongo.get_db()
    account = db.accounts.find_one({"username" : username})
    account["enabled"] = False
    db.accounts.save(account)
    return account

def _get_servers():
    db = quorum.mongo.get_db()
    servers = db.servers.find({
        "enabled" : True,
        "instance_id" : flask.session["instance_id"]
    })
    servers = [_build_server(server) for server in servers]
    return servers

def _get_all_servers():
    db = quorum.mongo.get_db()
    servers = db.servers.find({
        "enabled" : True
    })
    servers = [_build_server(server) for server in servers]
    return servers

def _get_server(name, build = True, raise_e = True):
    db = quorum.mongo.get_db()
    server = db.servers.find_one({
        "instance_id" : flask.session["instance_id"],
        "name" : name
    })
    if not server and raise_e: raise RuntimeError("Server not found")
    build and _build_server(server)
    return server

def _save_server(server):
    db = quorum.mongo.get_db()
    db.servers.save(server)
    return server

def _delete_server(name):
    db = quorum.mongo.get_db()
    server = db.servers.find_one({"name" : name})
    server["enabled"] = False
    db.servers.save(server)
    return server

def _get_log(name, start = 0, count = 6):
    pymongo = quorum.mongo.pymongo
    db = quorum.mongo.get_db()
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

def _validate_account_new():
    return [
        quorum.not_null("username"),
        quorum.not_empty("username"),
        quorum.not_duplicate("username", "accounts"),

        quorum.not_null("email"),
        quorum.not_empty("email"),
        quorum.not_duplicate("email", "accounts"),

        quorum.validation.not_null("password"),
        quorum.validation.not_empty("password"),

        quorum.not_null("email_confirm"),
        quorum.not_empty("email_confirm"),

        quorum.equals("email_confirm", "email")
    ] + _validate_account()

def _validate_account():
    return []

def _validate_server():
    return [
        quorum.not_null("name"),
        quorum.not_empty("name"),
        quorum.not_duplicate("name", "servers"),

        quorum.not_null("url"),
        quorum.not_empty("url"),

        quorum.not_null("description"),
        quorum.not_empty("description")
    ]

def _build_account(account):
    enabled = account.get("enabled", False)
    last_login = account.get("last_login", None)
    last_login_date = last_login and datetime.datetime.utcfromtimestamp(last_login)
    last_login_string = last_login_date and last_login_date.strftime("%d/%m/%Y %H:%M:%S")
    account["enabled_l"] = enabled and "enabled" or "disabled"
    account["last_login_l"] = last_login_string
    del account["password"]
    return account

def _build_server(server):
    up = server.get("up", False)
    server["up_l"] = up and "up" or "down"
    return server

def _build_log(log):
    up = log.get("up", False)
    timestamp = log.get("timestamp", None)
    date = datetime.datetime.utcfromtimestamp(timestamp)
    date_string = date.strftime("%d/%m/%Y %H:%M:%S")
    log["up_l"] = up and "up" or "down"
    log["date_l"] = date_string
    return log

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
    db = quorum.mongo.get_db()
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
    server["up"] = up
    server["latency"] = latency
    server["timestamp"] = start_time
    db.servers.save(server)

    # in case there's a change from server state up to down
    # must trigger the down event so that the user is notified
    if change_down: _event_down(server)

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
    import thread
    name = server.get("name", None)
    parameters = {
        "subject" : "Your %s server, is currently down" % name,
        "sender" : "Pingu Mailer <mailer@pingu.com>",
        "receivers" : ["João Magalhães <joamag@hive.pt>"],
        "plain" : "email/down.txt.tpl",
        "rich" : "email/down.html.tpl",
        "context" : {
            "server" : server
        }
    }
    thread.start_new_thread(_send_email, (), parameters)

def _render(template_name, **context):
    template = app.jinja_env.get_or_select_template(template_name)
    return flask.templating._render(template, context, app)

def _ensure_db():
    db = quorum.mongo.get_db()

    db.accounts.ensure_index("enabled")
    db.accounts.ensure_index("instance_id")
    db.accounts.ensure_index("username")
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

    db.log.ensure_index("name")
    db.log.ensure_index("up")
    db.log.ensure_index("timestamp")

def _setup_db():
    db = quorum.mongo.get_db()
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
        timeout = server.get("timeout", 5.0)
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
        current_time + timeout,
        _ping_m(server, timeout = timeout)
    )

def load():
    # sets the global wide application settings and
    # configures the application object according to
    # this settings
    debug = os.environ.get("DEBUG", False) and True or False
    app.debug = debug
    app.secret_key = SECRET_KEY

def run():
    # sets the debug control in the application
    # then checks the current environment variable
    # for the target port for execution (external)
    # and then start running it (continuous loop)
    debug = os.environ.get("DEBUG", False) and True or False
    reloader = os.environ.get("RELOADER", False) and True or False
    mongo_url = os.getenv("MONGOHQ_URL", MONGO_URL)
    smtp_host = os.environ.get("SMTP_HOST", "localhost")
    smtp_user = os.environ.get("SMTP_USER", None)
    smtp_password = os.environ.get("SMTP_PASSWORD", None)
    port = int(os.environ.get("PORT", 5000))
    quorum.mongo.url = mongo_url
    quorum.mongo.database = MONGO_DATABASE
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
