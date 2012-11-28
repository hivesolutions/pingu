{% extends "partials/layout.html.tpl" %}
{% block title %}Accounts{% endblock %}
{% block name %}Accounts{% endblock %}
{% block content %}
    <ul class="filter" data-no_input="1">
        <div class="data-source" data-url="/accounts.json" data-type="json" data-timeout="0"></div>
        <li class="template table-row">
            <div class="status text-left" data-width="80">%[username]</div>
            <div class="date text-left" data-width="160">%[last_login_l]</div>
            <div class="latency text-left" data-width="80">%[email]</div>
            <div class="latency text-right" data-width="260">%[login_count] times</div>
            <div class="clear"></div>
        </li>
        <div class="filter-no-results quote">
            no results found
        </div>
        <div class="filter-more">
            <span class="button">more</span>
        </div>
    </ul>
{% endblock %}