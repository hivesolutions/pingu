{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_link == "info" %}
            <a href="{{ url_for('show_account', username = account.username) }}" class="active">info</a>
        {% else %}
            <a href="{{ url_for('show_account', username = account.username) }}">info</a>
        {% endif %}
        //
        {% if sub_link == "edit" %}
            <a href="{{ url_for('edit_account', username = account.username) }}" class="active">edit</a>
        {% else %}
            <a href="{{ url_for('edit_account', username = account.username) }}">edit</a>
        {% endif %}
        //
        {% if sub_link == "delete" %}
            <a href="{{ url_for('delete_account', username = account.username) }}" class="active warning link-confirm"
               data-message="Do you really want to delete ?">delete</a>
        {% else %}
            <a href="{{ url_for('delete_account', username = account.username) }}" class="warning link-confirm"
               data-message="Do you really want to delete ?">delete</a>
        {% endif %}
    </div>
{% endblock %}
