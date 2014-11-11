{% extends "email/layout.html.tpl" %}
{% block title %}Your server {{ server.name }} is <span style="color: #c31f30">down</span>{% endblock %}
{% block content %}
<p>
    Pingu has unsuccessfully attempted to contact your {{ server.name }} server,
    and therefore considered it as down.
</p>
<p>
    It would be advisable to manually confirm that the service is actually down,
    and to perform the required measures to bring it back up.
</p>
<p>
    Pingu will be silently waiting for your server to come back, and will issue
    a notification back to you when it does.
</p>
{% endblock %}
