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

import datetime

import quorum

from pingu.models import base

class Log(base.Base):

    name = dict(
        index = True
    )

    url = dict(
        index = True
    )

    up = dict(
        type = bool,
        index = True
    )

    status = dict(
        index = True
    )

    reason = dict()

    latency = dict(
        type = int
    )

    timestamp = dict(
        type = float
    )

    @classmethod
    def validate(cls):
        return super(Log, cls).validate() + [
            quorum.not_null("url"),
            quorum.not_empty("url"),
            quorum.is_url("url"),

            quorum.not_null("up")
        ]

    @classmethod
    def validate_new(cls):
        return super(Log, cls).validate_new() + [
            quorum.not_null("name"),
            quorum.not_empty("name"),
            quorum.not_duplicate("name", "servers")
        ]

    @classmethod
    def _build(cls, model, map):
        base.Base._build(model, map)
        up = model.get("up", None)
        timestamp = model.get("timestamp", None)
        date = datetime.datetime.utcfromtimestamp(timestamp)
        date_string = date.strftime("%d/%m/%Y %H:%M:%S")
        model["up_l"] = up == True and "up" or up == False and "down" or "unknwon"
        model["date_l"] = date_string
