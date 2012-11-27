{% extends "partials/layout_server.html.tpl" %}
{% block title %}Servers{% endblock %}
{% block name %}{{ server.name }}{% endblock %}
{% block content %}
    <div class="quote">{{ server.description }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">status</td>
                <td class="left value {{ server.up_l }}" width="50%">{{ server.up_l }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">response time</td>
                <td class="left value" width="50%">{{ server.latency }} ms</td>
            </tr>
            <tr>
                <td class="right label" width="50%">url</td>
                <td class="left value" width="50%">{{ server.url }}</td>
            </tr>
        </tbody>
    </table>
{% endblock %}
