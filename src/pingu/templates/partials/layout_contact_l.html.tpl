{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_link == "list" %}
            <a href="{{ url_for('list_contacts') }}" class="active">list</a>
        {% else %}
            <a href="{{ url_for('list_contacts') }}">list</a>
        {% endif %}
        //
        {% if sub_link == "create" %}
            <a href="{{ url_for('new_contact') }}" class="active">create</a>
        {% else %}
            <a href="{{ url_for('new_contact') }}">create</a>
        {% endif %}
    </div>
{% endblock %}
