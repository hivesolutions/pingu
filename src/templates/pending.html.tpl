{% extends "partials/layout_simple.html.tpl" %}
{% block title %}Confirmation{% endblock %}
{% block name %}E-mail Confirmation{% endblock %}
{% block content %}
    <div class="quote">
        You should have received an email with information regarding
        <strong>account activation</strong>.<br />
        If you haven't received the email <a href="{{ url_for('resend') }}">click here</a>
        to re-send the email.
    </div>
{% endblock %}
