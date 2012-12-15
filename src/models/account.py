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
import hashlib
import datetime

import quorum

import base
import contact

PASSWORD_SALT = "pingu"
""" The salt suffix to be used during the encoding
of the password into an hash value """

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

class Account(base.Base):

    username = dict(
        index = True
    )

    password = dict(
        private = True
    )

    api_key = dict(
        private = True
    )

    confirmation = dict(
        private = True
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

    plan = dict(
        index = True
    )

    login_count = dict(
        type = int
    )

    last_login = dict(
        type = float
    )

    type = dict(
        type = int
    )

    tokens = dict(
        type = list
    )

    def __init__(self):
        base.Base.__init__(self)

    @classmethod
    def setup(cls):
        super(Account, cls).setup()

        # tries to find the root account (default) in case it's not
        # found returns immediately nothing to be done
        root = cls.find(username = "root")
        if root: return

        # encodes the provided password into an sha1 hash appending
        # the salt value to it before the encoding
        password = hashlib.sha1("root" + PASSWORD_SALT).hexdigest()
        instance_id = hashlib.sha1(str(uuid.uuid4())).hexdigest()

        # creates the structure to be used as the server description
        # using the values provided as parameters
        account = {
            "enabled" : True,
            "instance_id" : instance_id,
            "username" : "root",
            "password" : password,
            "plan" : "full",
            "email" : "root@pinguapp.com",
            "login_count" : 0,
            "last_login" : None,
            "type" : ADMIN_TYPE,
            "tokens" : USER_ACL.get(ADMIN_TYPE, ())
        }

        # saves the account instance into the data source, ensures
        # that the account is ready for login
        collection = cls._collection()
        collection.save(account)

    @classmethod
    def validate_new(cls):
        return base.Base.validate_new() + [
            quorum.not_null("username"),
            quorum.not_empty("username"),
            quorum.string_gt("username", 4),
            quorum.string_lt("username", 20),
            quorum.not_duplicate("username", cls._name()),

            quorum.validation.not_null("password"),
            quorum.validation.not_empty("password"),

            quorum.validation.not_null("password_confirm"),
            quorum.validation.not_empty("password_confirm"),

            quorum.not_null("email"),
            quorum.not_empty("email"),
            quorum.is_email("email"),
            quorum.not_duplicate("email", cls._name()),

            quorum.not_null("email_confirm"),
            quorum.not_empty("email_confirm"),

            quorum.not_null("plan"),
            quorum.not_empty("plan"),
            quorum.is_in("plan", ("basic", "advanced")),

            quorum.equals("password_confirm", "password"),
            quorum.equals("email_confirm", "email")
        ]

    @classmethod
    def _build(cls, model, map):
        quorum.Model._build(model, map)
        enabled = model.get("enabled", False)
        email = model.get("email", None)
        last_login = model.get("last_login", None)
        last_login_date = last_login and datetime.datetime.utcfromtimestamp(last_login)
        last_login_string = last_login_date and last_login_date.strftime("%d/%m/%Y %H:%M:%S")
        model["enabled_l"] = enabled and "enabled" or "disabled"
        model["email_s"] = email and email.replace("@", " at ").replace(".", " dot ")
        model["last_login_l"] = last_login_string
        model["email_md5"] = email and hashlib.md5(email).hexdigest()
        return model

    def pre_create(self):
        base.Base.pre_create(self)

        # "encrypts" the password into the target format defined
        # by the salt and the sha1 hash function and then creates
        # the api key for the current account
        self.password = hashlib.sha1(self.password + PASSWORD_SALT).hexdigest()
        self.api_key = hashlib.sha1(str(uuid.uuid4())).hexdigest()
        self.confirmation = hashlib.sha1(str(uuid.uuid4())).hexdigest()

        # updates the various default values for the current account
        # user to be created
        self.enabled = False
        self.instance_id = hashlib.sha1(str(uuid.uuid4())).hexdigest()
        self.login_count = 0
        self.last_login = None
        self.type = USER_TYPE
        self.tokens =  USER_ACL.get(USER_TYPE, ())

    def pre_update(self):
        base.Base.pre_update(self)

        # in case the currently set password is empty it must
        # be removed (not meant to be updated)
        if self.password == "": del self.password

    def post_create(self):
        base.Base.post_create(self)

        # creates the structure to be used as the contact description
        # using account values just created and then saves it in the
        # current data store
        contact_m = {
            "instance_id" : self.instance_id,
            "name" : self.username,
            "email" : self.email
        }
        contact_m = contact.Contact.new(model = contact_m)
        contact_m.save()

        # runs the post operation for the preparation of the confirm
        # of the account (must send appropriate documents: email, etc.)
        self.confirm()

    def confirm(self):
        # creates a new account in order to obtain the new build
        # values (include obfuscated email value) restores the
        # confirmation values that has been removed (private value)
        account = self.copy(build = True)
        account.confirmation = self.confirmation

        # sends a mail about the confirmation of the email to the
        # the email address associated with the current account
        quorum.send_mail_a(
            subject = "Welcome to Pingu, please confirm you email",
            sender = "Pingu Mailer <mailer@pinguapp.com>",
            receivers = ["%s <%s>" % (self.username, self.email)],
            plain = "email/confirm.txt.tpl",
            rich = "email/confirm.html.tpl",
            context = {
                "account" : account
            }
        )
