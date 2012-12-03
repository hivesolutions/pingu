{% extends "partials/layout_contact_l.html.tpl" %}
{% block title %}Contact{% endblock %}
{% block name %}New Contact{% endblock %}
{% block content %}
    <form action="{{ url_for('create_contact') }}" method="post" class="form">
        <div class="label label-left">
            <label>Name</label>
        </div>
        <div class="input">
            <input class="text-field focus" name="name" autocomplete="off" value="{{ contact.name }}"
                   data-error="{{ errors.name }}" />
        </div>
        <div class="label label-left">
            <label>E-mail</label>
        </div>
        <div class="input">
            <input class="text-field" name="email" autocomplete="off" value="{{ contact.email }}"
                   data-error="{{ errors.email }}" />
        </div>
        <div class="label label-left">
            <label>Phone</label>
        </div>
        <div class="input">
            <input class="text-field" name="phone" autocomplete="off" value="{{ contact.phone }}"
                   data-error="{{ errors.phone }}" />
        </div>
        <div class="label label-left">
            <label>XMPP</label>
        </div>
        <div class="input">
            <input class="text-field" name="xmpp" autocomplete="off" value="{{ contact.xmpp }}"
                   data-error="{{ errors.xmpp }}" />
        </div>
        <div class="label label-left">
            <label>Twitter</label>
        </div>
        <div class="input">
            <input class="text-field" name="twitter" autocomplete="off" value="{{ contact.twitter }}"
                   data-error="{{ errors.twitter }}" />
        </div>
        <div class="label label-left">
            <label>Facebook</label>
        </div>
        <div class="input">
            <input class="text-field" name="facebook" autocomplete="off" value="{{ contact.facebook }}"
                   data-error="{{ errors.facebook }}" />
        </div>
        <div class="quote">
            By clicking Create Contact, you agree to our Service Agreement and that you have
            read and understand our Privacy Policy.
        </div>
        <span class="button" data-submit="true">Create Contact</span>
    </form>
{% endblock %}
