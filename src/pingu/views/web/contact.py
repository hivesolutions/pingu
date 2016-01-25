#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Pingu System
# Copyright (c) 2008-2016 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

from pingu import models

from pingu.main import app
from pingu.main import flask
from pingu.main import quorum

@app.route("/contacts", methods = ("GET",))
@quorum.ensure("contacts.list")
def list_contacts():
    contacts = models.Contact.find_i()
    return flask.render_template(
        "contact/list.html.tpl",
        link = "contacts",
        sub_link = "list",
        contacts = contacts
    )

@app.route("/contacts/new", methods = ("GET",))
@quorum.ensure("contacts.new")
def new_contact():
    return flask.render_template(
        "contact/new.html.tpl",
        link = "contacts",
        sub_link = "create",
        contact = {},
        errors = {}
    )

@app.route("/contacts", methods = ("POST",))
@quorum.ensure("contacts.new")
def create_contact():
    # creates the new contact, using the provided arguments and
    # then saves it into the data source, all the validations
    # should be ran upon the save operation
    contact = models.Contact.new()
    try: contact.save()
    except quorum.ValidationError as error:
        return flask.render_template(
            "contact/new.html.tpl",
            link = "contacts",
            sub_link = "create",
            contact = error.model,
            errors = error.errors
        )

    # redirects the user to the show page of the contact that
    # was just created
    return flask.redirect(
        flask.url_for("show_contact", id = contact.id)
    )

@app.route("/contacts/<int:id>", methods = ("GET",))
@quorum.ensure("contacts.show")
def show_contact(id):
    contact = models.Contact.get_i(id = id)
    return flask.render_template(
        "contact/show.html.tpl",
        link = "contacts",
        sub_link = "info",
        contact = contact
    )

@app.route("/contacts/<int:id>/edit", methods = ("GET",))
@quorum.ensure("contacts.edit")
def edit_contact(id):
    contact = models.Contact.get_i(id = id)
    return flask.render_template(
        "contact/edit.html.tpl",
        link = "contacts",
        sub_link = "edit",
        contact = contact,
        errors = {}
    )

@app.route("/contacts/<int:id>/edit", methods = ("POST",))
@quorum.ensure("contacts.edit")
def update_contact(id):
    # finds the current contact and applies the provided
    # arguments and then saves it into the data source,
    # all the validations should be ran upon the save operation
    contact = models.Contact.get_i(id = id)
    contact.apply()
    try: contact.save()
    except quorum.ValidationError as error:
        return flask.render_template(
            "contact/edit.html.tpl",
            link = "contacts",
            sub_link = "edit",
            server = error.model,
            errors = error.errors
        )

    # redirects the user to the show page of the contact that
    # was just updated
    return flask.redirect(
        flask.url_for("show_contact", id = id)
    )

@app.route("/contacts/<int:id>/delete", methods = ("GET", "POST"))
@quorum.ensure("contacts.delete")
def delete_contact(id):
    contact = models.Contact.get_i(id = id)
    contact.delete()
    return flask.redirect(
        flask.url_for("list_contacts")
    )
