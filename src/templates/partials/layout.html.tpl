{% include "partials/doctype.html.tpl" %}
<head>
    {% block head %}
        {% include "partials/content_type.html.tpl" %}
        {% include "partials/includes.html.tpl" %}
        <title>Pingu / {% block title %}{% endblock %}</title>
    {% endblock %}
</head>
<body class="ux">
    <div id="overlay"></div>
    <div id="header">
        {% block header %}
            <h1>{% block name %}{% endblock %}</h1>
            <div class="links">
                {% if link == "home" %}
                    <a href="{{ url_for('index') }}" class="active">home</a>
                {% else %}
                    <a href="{{ url_for('index') }}">home</a>
                {% endif %}
                //
                {% if link == "servers" %}
                    <a href="{{ url_for('servers') }}" class="active">servers</a>
                {% else %}
                    <a href="{{ url_for('servers') }}">servers</a>
                {% endif %}
                //
                {% if link == "new_server" %}
                    <a href="{{ url_for('new_server') }}" class="active">new server</a>
                {% else %}
                    <a href="{{ url_for('new_server') }}">new server</a>
                {% endif %}
            </div>
        {% endblock %}
    </div>
    <div id="content">{% block content %}{% endblock %}</div>
    {% include "partials/footer.html.tpl" %}
</body>
{% include "partials/end_doctype.html.tpl" %}
