{% extends "partials/layout_contact_l.html.tpl" %}
{% block title %}Contacts{% endblock %}
{% block name %}Contacts{% endblock %}
{% block content %}
    <ul>
        {% for contact in contacts %}
            <li>
                <div class="name">
                    <a href="{{ url_for('show_contact', id = contact.id) }}">{{ contact.name }}</a>
                </div>
                <div class="description">{{ contact.email }}</div>
            </li>
        {% endfor %}
    </ul>
{% endblock %}
