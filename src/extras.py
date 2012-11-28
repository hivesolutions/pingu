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

import uuid
import json
import flask
import shelve
import pickle
import datetime
import functools

import werkzeug.datastructures

try: import redis
except: pass

YEAR_IN_SECS = 31536000
""" The number of seconds that exist in a
complete year (365 days) """

class RedisMemory:
    """
    "Local" in memory stub object that simulates
    the redis interface, useful for debugging.

    This memory interface may create problems in
    a multiple process environment (non shared memory).
    """

    values = None
    """ The map containing the various values to
    be set in the memory map, simulates the redis
    data store """

    def __init__(self):
        self.values = {}

    def get(self, name):
        name_s = str(name)
        return self.values.get(name_s)

    def set(self, name, value):
        name_s = str(name)
        self.values[name_s] = value

    def setex(self, name, value, expire):
        self.set(name, value)

    def delete(self, name):
        if not name in self.values: return
        del self.values[name]

class RedisShelve(RedisMemory):
    """
    "Local" in persistent stub object that simulates
    the redis interface, useful for debugging.

    This shelve interface requires a writable path
    where its persistent file may be written.
    """

    def __init__(self, path = "redis.shelve"):
        RedisMemory.__init__(self)
        self.values = shelve.open(path)

    def close(self):
        self.values.close()

    def set(self, name, value):
        RedisMemory.set(self, name, value)
        self.values.sync()

    def delete(self, name):
        name_s = str(name)
        if not self.values.has_key(name_s): return
        del self.values[name_s]

class RedisSession(werkzeug.datastructures.CallbackDict, flask.sessions.SessionMixin):

    def __init__(self, initial = None, sid = None, new = False):
        def on_update(self): self.modified = True
        werkzeug.datastructures.CallbackDict.__init__(self, initial, on_update)

        self.sid = sid
        self.new = new
        self.modified = False

class RedisSessionInterface(flask.sessions.SessionInterface):

    serializer = pickle
    """ The serializer to be used for the values
    contained in the session (used on top of the class) """

    session_class = RedisSession
    """ The class to be used to encapsulate a session
    the generated object will be serialized """

    def __init__(self, _redis = None, prefix = "session:", url = None):
        if _redis == None:
            _redis = url and redis.from_url(url) or RedisShelve()

        self.redis = _redis
        self.prefix = prefix

    def generate_sid(self):
        return str(uuid.uuid4())

    def get_redis_expiration_time(self, app, session):
        if session.permanent: return app.permanent_session_lifetime
        return datetime.timedelta(days = 1)

    def get_seconds(self, delta):
        return (delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 10 ** 6) / 10 ** 6

    def open_session(self, app, request):
        # tries to retrieve the session identifier from the
        # application cookie (or from parameters) in case
        # none is found generates a new one using the default
        # strategy and returns a new session object with that
        # session identifier
        sid = request.args.get("sid", request.args.get("session_id"))
        sid = sid or request.form.get("sid", request.form.get("session_id"))
        sid = sid or request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid = sid)

        # tries to retrieve the session value from redis in
        # case the values is successfully found loads it using
        # the serializer and returns the session object
        value = self.redis.get(self.prefix + sid)
        if not value == None:
            data = self.serializer.loads(value)
            return self.session_class(data, sid = sid)

        # returns a new session object with an already existing
        # session identifier, but not found in data source (redis)
        return self.session_class(sid = sid, new = True)

    def save_session(self, app, session, response):
        # retrieves the domain associated with the cookie to
        # be able to correctly modify it
        domain = self.get_cookie_domain(app)

        if not session:
            self.redis.delete(self.prefix + session.sid)
            if session.modified: response.delete_cookie(
                app.session_cookie_name,
                domain = domain
            )
            return

        redis_expire = self.get_redis_expiration_time(app, session)
        cookie_expire = self.get_expiration_time(app, session)
        value = self.serializer.dumps(dict(session))
        total_seconds = self.get_seconds(redis_expire)
        self.redis.setex(
            self.prefix + session.sid,
            value,
            int(total_seconds)
        )

        response.set_cookie(
            app.session_cookie_name,
            session.sid,
            expires = cookie_expire,
            httponly = True,
            domain = domain
        )

class SSLify(object):
    """
    Secures your flask app by enabling the forcing
    of the protocol in the http connection.
    """

    def __init__(self, app, age = YEAR_IN_SECS, subdomains = False):
        """
        Constructor of the class.

        @type app: App
        @param app: The application object to be used in the
        in ssl operation for the forcing of the protocol.
        @type age: int
        @param age: The maximum age of the hsts operation.
        @type subdomains: bool
        @param subdomains: If subdomain should be allows as part
        of the security policy.
        """

        if not app == None:
            self.app = app
            self.hsts_age = age
            self.hsts_include_subdomains = subdomains

            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        """
        Configures the configured flask app to enforce ssl.

        @type app: App
        @param app: The application to be configured to enforce
        the ssl redirection support.
        """

        app.before_request(self.redirect_to_ssl)
        app.after_request(self.set_hsts_header)

    @property
    def hsts_header(self):
        """
        Returns the proper hsts policy.

        @rtype: String
        @return: The proper hsts policy string value.
        """

        hsts_policy = "max-age={0}".format(self.hsts_age)
        if self.hsts_include_subdomains: hsts_policy += "; includeSubDomains"

        return hsts_policy

    def redirect_to_ssl(self):
        """
        Redirect incoming requests to https.

        @rtype: Request
        @return: The changed request containing the redirect
        instruction in case it's required.
        """

        criteria = [
            flask.request.is_secure,
            self.app.debug,
            flask.request.headers.get("X-Forwarded-Proto", "http") == "https"
        ]

        if not any(criteria):
            if flask.request.url.startswith("http://"):
                url = flask.request.url.replace("http://", "https://", 1)
                request = flask.redirect(url)

                return request

    def set_hsts_header(self, response):
        """
        Adds hsts header to each response.
        This header should enable extra security options to be
        interpreted at the client side.

        @type response: Response
        @param response: The response to be used to set the hsts
        policy header.
        @rtype: Response
        @return: The changed response object, containing the strict
        transport security (hsts) header.
        """

        response.headers.setdefault("Strict-Transport-Security", self.hsts_header)
        return response

def ensure_login(token = None, json_s = False):
    if "username" in flask.session and not token: return None
    if "*" in flask.session.get("tokens", []): return None
    if token in flask.session.get("tokens", []): return None

    if json_s:
        return flask.Response(
            json.dumps({
                "exception" : {
                    "message" : "Not enough permissions for operation"
                }
            }),
            status = 403,
            mimetype = "application/json"
        )
    else:
        return flask.redirect(
            flask.url_for("login")
        )

def ensure_user(username):
    _username = flask.session.get("username", None)
    if not _username == None and username == _username: return
    raise RuntimeError("Permission denied")

def ensure_session(object):
    if object.get("sesion_id", None) == flask.session.get("session_id", None): return
    raise RuntimeError("Permission denied")

def ensure(token = None, json = False):

    def decorator(function):

        @functools.wraps(function)
        def interceptor(*args, **kwargs):
            ensure = ensure_login(token, json)
            if ensure: return ensure
            return function(*args, **kwargs)

        return interceptor

    return decorator
