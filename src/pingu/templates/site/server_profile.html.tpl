{% extends "site/partials/layout.html.tpl" %}
{% block title %}{{ server.name }}{% endblock %}
{% block content %}
    <div class="content-server">
        <div class="header-server">
            <h1>{{ server.name }}</h1>
            <h2>{{ server.url }}</h2>
        </div>
          <ul class="statistics-server">
            <li>
                <h2>Current Status</h2>
                <p class="{{ server.up_l }}">{{ server.up_l }}</p>
            </li>
            <li>
                <h2>Downtimes</h2>
                <p>350</p>
            </li>
            <li>
                <h2>Avg. Response</h2>
                <p>{{ server.latency }} <span class="subscript">ms</span></p>
            </li>
            <li>
                <h2>Queries</h2>
                <p>1543</p>
            </li>
        </ul>
        <div class="footer-server">
            <div class="button footer-logo" data-link="{{ url_for('index') }}"></div>
        </div>
    </div>
{% endblock %}
