{% extends "partials/layout_server.html.tpl" %}
{% block title %}Servers{% endblock %}
{% block name %}{{ server.name }} :: log{% endblock %}
{% block content %}
    <ul class="filter" data-no_input="1">
        <div class="data-source" data-url="/servers/{{ server.name }}/log.json" data-type="json" data-timeout="0"></div>
        <li class="template clear table-cell">
            <div class="name text-center %[up_l]" data-width="80">%[up_l]</div>
            <div class="date text-left" data-width="170">%[date_l]</div>
            <div class="latency text-left" data-width="80">%[latency] ms</div>
            <div class="latency text-right" data-width="260">New York, United States</div>
            <div class="clear"></div>
        </li>
        <div class="filter-no-results quote">
            No results found
        </div>
        <div class="filter-more">
            <span class="button">Load more</span>
        </div>
    </ul>
{% endblock %}
