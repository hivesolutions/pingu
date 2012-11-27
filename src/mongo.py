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

try: import pymongo
except: pymongo = None

connection = None
""" The global connection object that should persist
the connection relation with the database service """

url = "mongodb://localhost:27017"
""" The global variable containing the url to be used
for the connection with the service """

database = "master"
""" The global variable containing the value for the
database to be used in the connection with the service """

def get_connection():
    global connection
    if pymongo == None: return None
    if not connection: connection = pymongo.Connection(url)
    return connection

def get_db():
    connection = get_connection()
    if not connection: return None
    result = pymongo.uri_parser.parse_uri(url)
    _database = result.get("database", None) or database
    db = connection[_database]
    return db
