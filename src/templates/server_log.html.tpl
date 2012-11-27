{% extends "partials/layout_server.html.tpl" %}
{% block title %}Servers{% endblock %}
{% block name %}{{ server.name }} :: log{% endblock %}
{% block content %}
    <ul>
        {% for _log in log %}
            <li>
                <div class="name">
                    {{ _log.up }}
                </div>
                <div class="description">
                    {{ _log.timestamp }}
                </div>
            </li>
        {% endfor %}
    </ul>
{% endblock %}
