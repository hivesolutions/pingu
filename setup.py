#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Pingu System
# Copyright (c) 2008-2016 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import setuptools

setuptools.setup(
    name = "pingu",
    version = "0.1.0",
    author = "Hive Solutions Lda.",
    author_email = "development@hive.pt",
    description = "Pingu Web Interface",
    license = "Apache License, Version 2.0",
    keywords = "pingu server control system",
    url = "http://pingu.com",
    zip_safe = False,
    packages = [
        "pingu",
        "pingu.models",
        "pingu.views",
        "pingu.views.api",
        "pingu.views.web"
    ],
    package_dir = {
        "" : os.path.normpath("src")
    },
    package_data = {
        "pingu" : [
            "heroku/*",
            "static/css/*",
            "static/fonts/*",
            "static/images/*.png",
            "static/images/*.ico",
            "static/images/site/*.png",
            "static/js/*",
            "templates/*.tpl",
            "templates/account/*.tpl",
            "templates/contact/*.tpl",
            "templates/email/*.tpl",
            "templates/partials/*.tpl",
            "templates/server/*.tpl",
            "templates/site/*.tpl"
        ]
    },
    install_requires = [
        "flask",
        "quorum",
        "pymongo",
        "redis"
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ]
)
