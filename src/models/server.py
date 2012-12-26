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

import quorum

import base
import task

DEFAULT_TIMEOUT = 60.0
""" The default timeout value to be used in between "ping"
requests, this values is only used as a fallback """

class Server(base.Base):

    name = dict(
        index = True
    )

    url = dict(
        index = True
    )

    description = dict()

    up = dict(
        type = bool,
        index = True
    )

    latency = dict(
        type = int
    )

    timestamp = dict(
        type = float
    )

    @classmethod
    def validate(cls):
        return super(Server, cls).validate() + [
            quorum.not_null("url"),
            quorum.not_empty("url"),
            quorum.is_url("url"),

            quorum.not_null("description"),
            quorum.not_empty("description")
        ]

    @classmethod
    def validate_new(cls):
        return super(Server, cls).validate_new() + [
            quorum.not_null("name"),
            quorum.not_empty("name"),
            quorum.not_duplicate("name", "servers")
        ]

    @classmethod
    def _build(cls, model, map):
        base.Base._build(model, map)
        up = model.get("up", None)
        model["up_l"] = up == True and "up" or up == False and "down" or "unknwon"

    def post_create(self):
        base.Base.post_create(self)

        # creates a task for the server that has just been created
        # this tuple is going to be used by the scheduling thread
        _task = task.Task(self, DEFAULT_TIMEOUT)

        # saves the server instance and schedules the task, this
        # should ensure coherence in the internal data structures
        _task.schedule()
