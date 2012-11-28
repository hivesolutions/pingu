{% extends "partials/layout_account.html.tpl" %}
{% block title %}Accounts{% endblock %}
{% block name %}{{ account.username }} :: edit{% endblock %}
{% block content %}
    <form action="{{ url_for('update_account', username = account.username) }}" method="post" class="form">
        <input type="hidden" name="_id" value="{{ account._id }}" />
        <div class="label label-left">
            <label>Username</label>
        </div>
        <div class="input">
            <input class="text-field" name="username" autocomplete="off" value="{{ account.username }}"
                   data-error="{{ errors.username }}" data-disabled="1" />
        </div>
        <div class="label label-left">
            <label>E-mail</label>
        </div>
        <div class="input">
            <input class="text-field" name="email" autocomplete="off" value="{{ account.email }}"
                   data-error="{{ errors.email }}" data-disabled="1" />
        </div>
        <div class="label label-left">
            <label>Password</label>
        </div>
        <div class="input">
            <input class="text-field" name="password" type="password" autocomplete="off"
                   value="{{ account.password }}" data-error="{{ errors.password }}" />
        </div>
        <div class="separator-horizontal"></div>
        <div class="label label-left">
            <label>Phone</label>
        </div>
        <div class="input">
            <input class="text-field" name="phone" autocomplete="off" value="{{ account.phone }}"
                   data-error="{{ errors.phone }}" />
        </div>
        <div class="label label-left">
            <label>Twitter</label>
        </div>
        <div class="input">
            <input class="text-field" name="twitter" autocomplete="off" value="{{ account.twitter }}"
                   data-error="{{ errors.twitter }}" />
        </div>
        <div class="label label-left">
            <label>Facebook</label>
        </div>
        <div class="input">
            <input class="text-field" name="facebook" autocomplete="off" value="{{ account.facebook }}"
                   data-error="{{ errors.twitter }}" />
        </div>
        <span class="button" data-link="{{ url_for('show_account', username = account.username) }}">Cancel</span>
        //
        <span class="button" data-submit="true">Update</span>
    </form>
{% endblock %}
