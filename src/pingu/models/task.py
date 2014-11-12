#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Pingu System
# Copyright (C) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import time

import quorum

from pingu.models import log
from pingu.models import base
from pingu.models import server
from pingu.models import contact

DEFAULT_TIMEOUT = 60.0
""" The default timeout value to be used in between "ping"
requests, this values is only used as a fallback """

TASKS = ()
""" The set of tasks to be executed by ping operations
this is the standard hardcoded values """

HEADERS = {
    "User-Agent" : "pingu/0.1.0",
    "X-Powered-By" : "hive-server/0.1.0"
}
""" The map of headers to be used as base for the pingu
http client to use """

class Task(base.Base):

    server = dict(
        index = True
    )

    timeout = dict(
        type = int
    )

    def __init__(self, server = None, timeout = DEFAULT_TIMEOUT):
        base.Base.__init__(self)
        self.server = server
        self.timeout = timeout

    @classmethod
    def get_all(cls):
        """
        Retrieves the complete set of tasks as a tuple of
        server and timeout for the current execution context.

        The returned value is global and should contain all
        the tasks in the data source.

        @rtype: List
        @return: The list containing the complete set of task
        tuples in the data source.
        """

        tasks = []
        servers = server.Server.find(enabled = True)
        for _server in servers:
            timeout = _server.val("timeout", DEFAULT_TIMEOUT)
            task = Task(_server, timeout)
            tasks.append(task)

        return tasks + list(TASKS)

    @classmethod
    def schedule_all(cls):
        # retrieves the current time and then iterates over
        # all the tasks to insert them into the execution thread
        tasks = Task.get_all()
        for task in tasks: task.schedule()

    def schedule(self):
        quorum.run_back(self.ping)

    def ping(self):
        # retrieves the server again to ensure that the data
        # is correct in it
        self.server = self.server.reload()

        # retrieves the various attribute values from the server
        # that are going to be used in the method
        instance_id = self.server.instance_id
        name = self.server.name
        url = self.server.url
        method = self.server.val("method", "GET")

        # parses the provided url values, retrieving the various
        # components of it to be used in the ping operation
        url_s = quorum.legacy.urlparse(url)
        scheme = url_s.scheme
        hostname = url_s.hostname
        port = url_s.port
        path = url_s.path

        # retrieves the connection class to be used according
        # to the scheme defined in the url
        connection_c = quorum.legacy.HTTPSConnection if\
            scheme == "https" else quorum.legacy.HTTPConnection

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
        quorum.debug("%s :: %s %s / %dms" % (url, status, reason, latency))

        # inserts the log document into the data source so that
        # the information is registered in the proper place
        _log = dict(
            enabled = True,
            instance_id = instance_id,
            name = name,
            url = url,
            up = up,
            status = status,
            reason = reason,
            latency = latency,
            timestamp = start_time
        )
        _log = log.Log.new(model = _log)
        _log.save()

        # verifies the correct changing orders (from up to down and
        # from down to up) this will trigger the proper events
        change_down = not self.server.val("up", True) == up and not up
        change_up = not self.server.val("up", True) == up and up

        # updates the server information, so that it matched the last
        # available information from the last "ping" operation
        self.server.up = up
        self.server.latency = latency
        self.server.timestamp = start_time
        self.server.save(server)

        # in case there's a change from server state up to down, or
        # down to up (reversed) must trigger the proper event so
        # that the user is notified about the change
        if change_down: self.on_down()
        if change_up: self.on_up()

        # retrieves the current time and uses that value to
        # re-insert a new task into the execution thread, this
        # is considered the re-schedule operation
        current_time = time.time()
        self.server.enabled and quorum.run_back(
            self.ping,
            target_time = current_time + self.timeout
        )

    def on_down(self):
        # retrieves the complete set of contacts and sends
        # an mail about the server down for the email to the
        # the various email addresses for notification
        instance_id = self.server.instance_id
        contacts = contact.Contact.find(enabled = True, instance_id = instance_id)
        for _contact in contacts:
            quorum.send_mail_a(
                subject = "Your server %s, is currently down" % self.server.name,
                sender = "Pingu Mailer <mailer@pinguapp.com>",
                receivers = ["%s <%s>" % (_contact.name, _contact.email)],
                plain = "email/down.txt.tpl",
                rich = "email/down.html.tpl",
                context = dict(
                    server = server
                )
            )

    def on_up(self):
        # retrieves the complete set of contacts and sends
        # an mail about the server up for the email to the
        # the various email addresses for notification
        instance_id = self.server.instance_id
        contacts = contact.Contact.find(enabled = True, instance_id = instance_id)
        for _contact in contacts:
            quorum.send_mail_a(
                subject = "Your server %s, is back online" % self.server.name,
                sender = "Pingu Mailer <mailer@pinguapp.com>",
                receivers = ["%s <%s>" % (_contact.name, _contact.email)],
                plain = "email/up.txt.tpl",
                rich = "email/up.html.tpl",
                context = dict(
                    server = server
                )
            )
