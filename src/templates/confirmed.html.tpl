{% extends "partials/layout_simple.html.tpl" %}
{% block title %}Confirmed{% endblock %}
{% block name %}Account Confirmed{% endblock %}
{% block content %}
    <div class="quote">
        You account is now confirmed you can now start using
        Ping by going to <a href="{{ url_for('index') }}">login page</a>.
    </div>
{% endblock %}
