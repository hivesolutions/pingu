{% extends "email/layout.txt.tpl" %}
{% block title %}Welcome to Pingu{% endblock %}
{% block content %}
Welcome to Pingu! You are one step away from having 24/7, hassle-free,
constant monitoring of your services.

Just click on the following link [https://pinguapp.com/confirm/{{ account.confirmation }}] to activate your
account and start using Pingu.

username // {{ account.username }}
email // {{ account.email_s }}
plan // {{ account.plan }}

Thanks,
The Pingu Team
{% endblock %}
