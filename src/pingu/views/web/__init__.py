#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Pingu System
# Copyright (C) 2008-2015 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

from . import account
from . import base
from . import contact
from . import heroku
from . import server

from .account import list_accounts, list_accounts_json, new_account, create_account,\
    create_account_json, show_account, edit_account, update_account, delete_account
from .base import home, docs_api, index, about, pending, resend, confirm, signin,\
    login, logout
from .contact import list_contacts, new_contact, create_contact, show_contact, edit_contact,\
    update_contact, delete_contact
from .heroku import create_servers_h, get_navbar_h, provision, deprovision, plan_change,\
    sso_login
from .server import list_servers, new_server, create_server, show_server, edit_server,\
    update_server, delete_server, list_log, list_log_json, profile_server, badge_server
