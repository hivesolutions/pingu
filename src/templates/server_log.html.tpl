{% extends "partials/layout_server.html.tpl" %}
{% block title %}Servers{% endblock %}
{% block name %}{{ server.name }} :: log{% endblock %}
{% block content %}
    <ul class="filter" data-no_input="1">
        <div class="data-source" data-url="{{ url_for('list_log_json', name = server.name) }}" data-type="json" data-timeout="0"></div>
        <li class="template table-row">
            <div class="status text-left %[up_l]" data-width="56">%[up_l]</div>
            <div class="date text-left" data-width="160">%[date_l]</div>
            <div class="latency text-left" data-width="80">%[latency] ms</div>
            <div class="latency text-right" data-width="284">New York, United States</div>
            <div class="table-clear"></div>
        </li>
        <div class="filter-no-results quote">
            No results found
        </div>
        <div class="filter-more">
            <span class="button more">Load more</span>
            <span class="button load">Loading</span>
        </div>
    </ul>
{% endblock %}
