{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_link == "list" %}
            <a href="{{ url_for('list_servers') }}" class="active">list</a>
        {% else %}
            <a href="{{ url_for('list_servers') }}">list</a>
        {% endif %}
        //
        {% if sub_link == "create" %}
            <a href="{{ url_for('new_server') }}" class="active">create</a>
        {% else %}
            <a href="{{ url_for('new_server') }}">create</a>
        {% endif %}
    </div>
{% endblock %}
