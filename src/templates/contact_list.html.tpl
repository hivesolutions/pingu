{% extends "partials/layout_contact_l.html.tpl" %}
{% block title %}Contacts{% endblock %}
{% block name %}Contacts{% endblock %}
{% block content %}
    <ul>
        {% for contact in contacts %}
            <li>
            	<div class="image">
            		<img src="http://www.gravatar.com/avatar/{{ contact.email_md5 }}.jpg?size=64" width="64" height="64" />
            	</div>
                <div class="name">
                    <a href="{{ url_for('show_contact', id = contact.id) }}">{{ contact.name }}</a>
                </div>
                <div class="description">{{ contact.email }}</div>
            </li>
        {% endfor %}
    </ul>
{% endblock %}
