{% extends "partials/layout.html.tpl" %}
{% block title %}Servers{% endblock %}
{% block name %}New Server{% endblock %}
{% block content %}
    <form action="{{ url_for('create_server') }}" method="post" class="form">
        <div class="label">
            <label>Server Name</label>
        </div>
        <div class="input">
            <input class="text-field focus" name="name" placeholder="eg: colony" value="{{ server.name }}"
                   data-error="{{ errors.name }}" />
        </div>
        <div class="label">
            <label>URL</label>
        </div>
        <div class="input">
            <input class="text-field" name="url" placeholder="eg: http://getcolony.com" value="{{ server.url }}"
                   data-error="{{ errors.url }}" />
        </div>
        <div class="label">
            <label>Description</label>
        </div>
        <div class="input">
            <textarea class="text-area" name="description" placeholder="eg: some words about the server"
                      data-error="{{ errors.description }}">{{ server.description }}</textarea>
        </div>
        <div class="quote">
            By clicking Submit Server, you agree to our Service Agreement and that you have
            read and understand our Privacy Policy.
        </div>
        <span class="button" data-submit="true">Submit Server</span>
    </form>
{% endblock %}
