{% extends "email/layout.html.tpl" %}
{% block title %}Your server {{ server.name }} is <span style="color: #32951b">up</span>{% endblock %}
{% block content %}
<p>
    Pingu has previously detected a service downtime and has been patiently
    waiting for its return. After being able to successfully contact your
    server, it has been marked as being up again.
</p>
<p>
    In case this service failure and recovery was unexpected, it would be
    advisable to investigate the reasons for this unexpected downtime.
</p>
<p>
    Pingu will continue to actively monitor your server, and will notify
    you immediately if it ever goes down again.
</p>
{% endblock %}
