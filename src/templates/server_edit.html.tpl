{% extends "partials/layout_server.html.tpl" %}
{% block title %}Servers{% endblock %}
{% block name %}{{ server.name }} :: edit{% endblock %}
{% block content %}
    <form action="{{ url_for('update_server', name = server.name) }}" method="post" class="form">
        <input type="hidden" name="_id" value="{{ server._id }}" />
        <div class="label">
            <label>Server Name</label>
        </div>
        <div class="input">
            <input class="text-field" name="name" placeholder="eg: colony" value="{{ server.name }}"
                   data-error="{{ errors.name }}" data-disabled="1" />
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
        <span class="button" data-link="{{ url_for('show_server', name = server.name) }}">Cancel</span>
        //
        <span class="button" data-submit="true">Update</span>
    </form>
{% endblock %}
