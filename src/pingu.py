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
import httplib
import urlparse

import execution

SECRET_KEY = "kyjbqt4828ky8fdl7ifwgawt60erk8wg"
""" The "secret" key to be at the internal encryption
processes handled by flask (eg: sessions) """

TASKS = (
    ("http://www.sapo.pt/", "GET", 10.0),
    ("http://www.google.pt/", "GET", 30.0),
    ("https://app.frontdoorhq.com", "GET", 5.0),
)
""" The set of tasks to be executed by ping operations
this is the standard hardcoded values """

app = flask.Flask(__name__)
#app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(365)
#app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
#app.config["MAX_CONTENT_LENGTH"] = 1024 ** 3

@app.route("/", methods = ("GET",))
@app.route("/index", methods = ("GET",))
def index():
    return flask.render_template(
        "index.html.tpl",
        link = "home"
    )

def _ping(url = None, method = "GET", timeout = 1.0):
    # creates the map that hold the various headers
    # to be used in the http connection
    headers = {
        "User-Agent" : "pingu/0.1.0"
    }

    # parses the provided url values, retrieving the various
    # components of it to be used in the ping operation
    url_s = urlparse.urlparse(url)
    host = url_s.netloc
    port = url_s.port
    path = url_s.path

    # retrieves the timestamp for the start of the connection
    # to the remote host and then creates a new connection to
    # the remote host to proceed with the "ping" operation
    start_time = time.time()
    connection = httplib.HTTPConnection(host, port)
    try:
        connection.request(method, path, headers = headers)
        response = connection.getresponse()
    finally:
        connection.close()
    end_time = time.time()
    latency = (end_time - start_time) * 1000.0

    # prints a debug message about the ping operation
    # with the complete diagnostics information
    print "%s :: %s %s / %dms" % (url, response.status, response.reason, latency)

    current_time = time.time()
    execution_thread.insert_work(
        current_time + timeout,
        _ping_m(url, method = method, timeout = timeout)
    )

def _ping_m(url, method = "GET", timeout = 1.0):
    def _pingu(): _ping(url, method = method, timeout = timeout)
    return _pingu

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
    port = int(os.environ.get("PORT", 5000))
    app.debug = debug
    app.secret_key = SECRET_KEY
    app.run(
        use_debugger = debug,
        debug = debug,
        use_reloader = reloader,
        host = "0.0.0.0",
        port = port
    )

# creates the thread that it's going to be used to
# execute the various background tasks and starts
# it, providing the mechanism for execution
execution_thread = execution.ExecutionThread()
execution_thread.start()

# retrieves the current time and then iterates over
# all the tasks to insert them into the execution thread
current_time = time.time()
for task in TASKS:
    url, method, timeout = task
    execution_thread.insert_work(
        current_time + timeout,
        _ping_m(url, method = method, timeout = timeout)
    )

if __name__ == "__main__": run()
else: load()
