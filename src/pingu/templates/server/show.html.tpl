{% extends "partials/layout_server.html.tpl" %}
{% block title %}Servers{% endblock %}
{% block name %}{{ server.name }}{% endblock %}
{% block content %}
    <div class="quote">{{ server.name }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">status</td>
                <td class="left value {{ server.up_l }}" width="50%">{{ server.up_l|default("-", True) }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">response time</td>
                <td class="left value" width="50%">
                    {% if server.latency %}
                        {{ server.latency }} ms
                    {% else %}
                        -
                    {% endif %}
                </td>
            </tr>
            <tr>
                <td class="right label" width="50%">url</td>
                <td class="left value" width="50%">
                    {% if server.url %}
                        <a href="{{ server.url }}">{{ server.url }}</a>
                    {% else %}
                        -
                    {% endif %}
                </td>
            </tr>
        </tbody>
    </table>
{% endblock %}
