{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_link == "info" %}
            <a href="{{ url_for('show_server', name = server.name) }}" class="active">info</a>
        {% else %}
            <a href="{{ url_for('show_server', name = server.name) }}">info</a>
        {% endif %}
        //
        {% if sub_link == "edit" %}
            <a href="{{ url_for('edit_server', name = server.name) }}" class="active">edit</a>
        {% else %}
            <a href="{{ url_for('edit_server', name = server.name) }}">edit</a>
        {% endif %}
        //
        {% if sub_link == "delete" %}
            <a href="{{ url_for('delete_server', name = server.name) }}" class="active">delete</a>
        {% else %}
            <a href="{{ url_for('delete_server', name = server.name) }}">delete</a>
        {% endif %}
    </div>
{% endblock %}
