{% extends "email/layout.html.tpl" %}
{% block title %}Welcome to Pingu{% endblock %}
{% block content %}
<p>
    Welcome to Pingu! You are one step away from having 24/7, hassle-free,
    constant monitoring of your services.
</p>
<p>
    Just click on the following <a href="https://pinguapp.com/confirm/{{ account.confirmation }}">link</a> to activate
    your account and start using Pingu.
</p>
<p>
    username // <strong>{{ account.username }}</strong><br/>
    email // <strong>{{ account.email_s }}</strong><br/>
    plan // <strong>{{ account.plan }}</strong>
</p>
<p>
    Thanks,<br />
    The Pingu Team
</p>
{% endblock %}
