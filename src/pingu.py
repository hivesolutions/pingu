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
import time
import flask
import mongo
import atexit
import httplib
import smtplib
import datetime
import urlparse

import email.mime.multipart
import email.mime.text

import config
import execution

SECRET_KEY = "kyjbqt4828ky8fdl7ifwgawt60erk8wg"
""" The "secret" key to be at the internal encryption
processes handled by flask (eg: sessions) """

TASKS = ()
""" The set of tasks to be executed by ping operations
this is the standard hardcoded values """

MONGO_URL = "mongodb://localhost:27017"
""" The default url to be used for the connection with
the mongo database """

MONGO_DATABASE = "pingu"
""" The default database to be used for the connection with
the mongo database """

app = flask.Flask(__name__)
#app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(365)
#app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
#app.config["MAX_CONTENT_LENGTH"] = 1024 ** 3

mongo_url = os.getenv("MONGOHQ_URL", MONGO_URL)
mongo.url = mongo_url
mongo.database = MONGO_DATABASE

@app.route("/", methods = ("GET",))
@app.route("/index", methods = ("GET",))
def index():
    return flask.render_template(
        "index.html.tpl",
        link = "home"
    )

@app.route("/about", methods = ("GET",))
def about():
    return flask.render_template(
        "about.html.tpl",
        link = "about"
    )

@app.route("/servers", methods = ("GET",))
def servers():
    # retrieves the various entries from the servers
    # folder as the various servers
    servers = _get_servers()
    return flask.render_template(
        "server_list.html.tpl",
        link = "servers",
        servers = servers
    )

@app.route("/servers/new", methods = ("GET",))
def new_server():
    return flask.render_template(
        "server_new.html.tpl",
        link = "new_server"
    )

@app.route("/servers", methods = ("POST",))
def create_server():
    return update_server()

@app.route("/servers/<name>", methods = ("GET",))
def show_server(name):
    server = _get_server(name)
    return flask.render_template(
        "server_show.html.tpl",
        link = "servers",
        sub_link = "info",
        server = server
    )

@app.route("/servers/<name>/edit", methods = ("GET",))
def edit_server(name):
    server = _get_server(name)
    return flask.render_template(
        "server_edit.html.tpl",
        link = "servers",
        sub_link = "edit",
        server = server
    )

@app.route("/servers/<name>/edit", methods = ("POST",))
def update_server(name = None):
    # retrieves all the parameters from the request to be
    # handled then validated the required ones
    _name = flask.request.form.get("name", None)
    url = flask.request.form.get("url", None)
    description = flask.request.form.get("description", None)

    # sets the validation method in the various attributes
    # coming from the client form
    not_null(_name) and not_empty(_name)
    not_null(url) and not_empty(url)
    not_null(description) and not_empty(description)

    # creates the structure to be used as the server description
    # using the values provided as parameters
    server = name and _get_server(name) or {}
    enabled = server.get("enabled", True)
    server["enabled"] = enabled
    server["name"] = _name
    server["url"] = url
    server["description"] = description

    # creates a task for the server that has just been created
    # this tuple is going to be used by the scheduling thread
    task = (_name, url, "GET", 5.0)

    # saves the server instance and schedules the task, this
    # should ensure coherence in the internal data structures
    _save_server(server)
    not name and _schedule_task(task)

    # redirects the user to the show page of the server that
    # was just created
    return flask.redirect(
        flask.url_for("show_server", name = _name)
    )

@app.route("/servers/<name>/delete", methods = ("GET", "POST"))
def delete_server(name):
    _delete_server(name)
    return flask.redirect(
        flask.url_for("servers")
    )

@app.route("/servers/<name>/log", methods = ("GET",))
def log_server(name):
    server = _get_server(name)
    log = _get_log(name)
    return flask.render_template(
        "server_log.html.tpl",
        link = "servers",
        sub_link = "log",
        server = server,
        log = log
    )

@app.route("/servers/<name>/log.json", methods = ("GET",))
def log_server_json(name):
    start_record = int(flask.request.args.get("start_record", 0))
    number_records = int(flask.request.args.get("number_records", 5))
    log = _get_log(name, start = start_record, count = number_records)

    return flask.Response(
        mongo.dumps(log),
        mimetype = "application/json"
    )

def not_null(value):
    if not value == None: return True
    raise RuntimeError("value is not set")

def not_empty(value):
    if len(value): return True
    raise RuntimeError("value is empty")

def _get_servers():
    db = mongo.get_db()
    servers = db.server.find({"enabled" : True})
    return servers

def _get_server(name):
    db = mongo.get_db()
    server = db.server.find_one({"name" : name})
    _build_server(server)
    return server

def _save_server(server):
    db = mongo.get_db()
    db.server.save(server)
    return server

def _delete_server(name):
    db = mongo.get_db()
    server = db.server.find_one({"name" : name})
    server["enabled"] = False
    db.server.save(server)
    return server

def _get_log(name, start = 0, count = 5):
    db = mongo.get_db()
    log = db.log.find(
        {"name" : name},
        skip = start,
        limit = count,
        sort = [("timestamp", mongo.pymongo.DESCENDING)]
    )
    log_b = []
    for _log in log: _build_log(_log); log_b.append(_log)
    return log_b

def _build_server(server):
    up = server.get("up", False)
    server["up_l"] = up and "up" or "down"

def _build_log(log):
    up = log.get("up", False)
    timestamp = log.get("timestamp", None)
    date = datetime.datetime.utcfromtimestamp(timestamp)
    date_string = date.strftime("%d/%m/%Y %H:%M:%S")
    log["up_l"] = up and "up" or "down"
    log["date_l"] = date_string

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

def _ping(name, url = None, method = "GET", timeout = 1.0):
    # creates the map that hold the various headers
    # to be used in the http connection
    headers = {
        "User-Agent" : "pingu/0.1.0"
    }

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
        connection.request(method, path, headers = headers)
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
    db = mongo.get_db()
    db.log.insert({
        "enabled" : True,
        "name" : name,
        "url" : url,
        "up" : up,
        "status" : status,
        "reason" : reason,
        "latency" : latency,
        "timestamp" : start_time
    })

    server = db.server.find_one({"name" : name}) or {
        "name" : name
    }
    change_down = not server.get("up", True) == up and not up
    server["up"] = up
    server["latency"] = latency
    server["timestamp"] = start_time
    db.server.save(server)

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
        _ping_m(name, url, method = method, timeout = timeout)
    )

def _ping_m(name, url, method = "GET", timeout = 1.0):
    def _pingu(): _ping(name, url, method = method, timeout = timeout)
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
    db = mongo.get_db()

    db.log.ensure_index("name")
    db.log.ensure_index("up")
    db.log.ensure_index("timestamp")

    db.server.ensure_index("enabled")
    db.server.ensure_index("name")
    db.server.ensure_index("url")
    db.server.ensure_index("up")
    db.server.ensure_index("latency")
    db.server.ensure_index("timestamp")

def _get_tasks():
    tasks = []
    servers = _get_servers()

    for server in servers:
        name = server.get("name", None)
        url = server.get("url", None)
        method = server.get("method", "GET")
        timeout = server.get("timeout", 5.0)
        tasks.append((
            name,
            url,
            method,
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
    name, url, method, timeout = task
    execution_thread.insert_work(
        current_time + timeout,
        _ping_m(name, url, method = method, timeout = timeout)
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
    mongo.url = mongo_url
    mongo.database = MONGO_DATABASE
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
execution_thread = execution.ExecutionThread()
execution_thread.start()

# ensures the various requirements for the database
# so that it becomes ready for usage
_ensure_db()

# schedules the various tasks currently registered in
# the system internal structures
_schedule_tasks()

if __name__ == "__main__": run()
else: load()
