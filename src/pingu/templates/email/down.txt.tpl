{% extends "email/layout.txt.tpl" %}
{% block title %}Your server {{ server.name }} is down{% endblock %}
{% block content %}
Pingu has unsuccessfully attempted to contact your {{ server.name }} server,
and therefore considered it as down.

It would be advisable to manually confirm that the service is actually down,
and to perform the required measures to bring it back up.

Pingu will be silently waiting for your server to come back, and will issue
a notification back to you when it does.
{% endblock %}
