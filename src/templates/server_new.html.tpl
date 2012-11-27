{% extends "partials/layout.html.tpl" %}
{% block title %}Servers{% endblock %}
{% block name %}New Server{% endblock %}
{% block content %}
    <form action="{{ url_for('create_server') }}" method="post" class="form">
        <div class="label">
            <label>Server Name</label>
        </div>
        <div class="input">
            <input name="name" placeholder="eg: colony" />
        </div>
        <div class="label">
            <label>URL</label>
        </div>
        <div class="input">
            <input name="url" placeholder="eg: http://getcolony.com" />
        </div>
        <div class="label">
            <label>Description</label>
        </div>
        <div class="input">
            <textarea name="description" placeholder="eg: some words about the server"></textarea>
        </div>
        <div class="quote">
            By clicking Submit Server, you agree to our Service Agreement and that you have
            read and understand our Privacy Policy.
        </div>
        <span class="button" data-submit="true">Submit Server</span>
    </form>
{% endblock %}
