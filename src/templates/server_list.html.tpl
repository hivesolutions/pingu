{% extends "partials/layout.html.tpl" %}
{% block title %}Servers{% endblock %}
{% block name %}Servers{% endblock %}
{% block content %}
    <ul>
        {% for server in servers %}
            <li>
                <div class="name">
                    <a href="{{ url_for('show_server', name = server.name) }}">{{ server.name }}</a>
                </div>
                <div class="description">
                    {{ server.url }}
                </div>
            </li>
        {% endfor %}
    </ul>
{% endblock %}
