{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_link == "info" %}
            <a href="{{ url_for('show_contact', id = contact.id) }}" class="active">info</a>
        {% else %}
            <a href="{{ url_for('show_contact', id = contact.id) }}">info</a>
        {% endif %}
        //
        {% if sub_link == "edit" %}
            <a href="{{ url_for('edit_contact', id = contact.id) }}" class="active">edit</a>
        {% else %}
            <a href="{{ url_for('edit_contact', id = contact.id) }}">edit</a>
        {% endif %}
        //
        {% if sub_link == "delete" %}
            <a href="{{ url_for('delete_contact', id = contact.id) }}" class="active">delete</a>
        {% else %}
            <a href="{{ url_for('delete_contact', id = contact.id) }}">delete</a>
        {% endif %}
    </div>
{% endblock %}
