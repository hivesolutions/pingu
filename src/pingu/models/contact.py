#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Pingu System
# Copyright (c) 2008-2020 Hive Solutions Lda.
#
# This file is part of Hive Pingu System.
#
# Hive Pingu System is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Pingu System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Pingu System. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import hashlib

import quorum

from . import base

class Contact(base.Base):

    name = dict(
        index = True
    )

    email = dict(
        index = True
    )

    phone = dict(
        index = True
    )

    xmpp = dict(
        index = True
    )

    twitter = dict(
        index = True
    )

    facebook = dict(
        index = True
    )

    @classmethod
    def validate(cls):
        return super(Contact, cls).validate() + [
            quorum.not_null("name"),
            quorum.not_empty("name"),

            quorum.not_null("email"),
            quorum.not_empty("email"),
            quorum.is_email("email")
        ]

    @classmethod
    def _build(cls, model, map):
        super(Contact, cls)._build(model, map)
        email = model.get("email", None)
        model["email_md5"] = email and hashlib.md5(quorum.legacy.bytes(email)).hexdigest()
