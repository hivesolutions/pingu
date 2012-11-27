{% extends "partials/layout_server.html.tpl" %}
{% block title %}Servers{% endblock %}
{% block name %}{{ server.name }} :: edit{% endblock %}
{% block content %}
    <form action="{{ url_for('update_server', name = server.name) }}" method="post" class="form">
        <div class="label">
            <label>Server Name</label>
        </div>
        <div class="input">
            <input name="name" value="{{ server.name }}" placeholder="eg: colony" />
        </div>
        <div class="label">
            <label>URL</label>
        </div>
        <div class="input">
            <input name="url" value="{{ server.url }}" placeholder="eg: http://getcolony.com" />
        </div>
        <div class="label">
            <label>Description</label>
        </div>
        <div class="input">
            <textarea name="description" placeholder="eg: some words about the server">{{ server.description }}</textarea>
        </div>
        <span class="button" data-link="{{ url_for('show_server', name = server.name) }}">Cancel</span>
        //
        <span class="button" data-submit="true">Update</span>
    </form>
{% endblock %}
