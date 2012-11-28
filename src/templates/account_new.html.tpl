{% extends "partials/layout.html.tpl" %}
{% block title %}Account{% endblock %}
{% block name %}New Account{% endblock %}
{% block content %}
    <form action="{{ url_for('create_account') }}" method="post" class="form">
        <div class="label label-left">
            <label>Username</label>
        </div>
        <div class="input">
            <input name="username" />
        </div>
        <div class="label label-left">
            <label>Password</label>
        </div>
        <div class="input">
            <input name="password" type="password" />
        </div>
        <div class="label label-left">
            <label>E-mail</label>
        </div>
        <div class="input">
            <input name="email" />
        </div>
        <div class="label label-left">
            <label>Confirm E-mail</label>
        </div>
        <div class="input">
            <input name="email_confirm" />
        </div>
        <div class="quote">
            By clicking Create Account, you agree to our Service Agreement and that you have
            read and understand our Privacy Policy.
        </div>
        <span class="button" data-submit="true">Create Account</span>
    </form>
{% endblock %}
