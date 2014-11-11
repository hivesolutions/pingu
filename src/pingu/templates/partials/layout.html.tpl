{% include "partials/doctype.html.tpl" %}
<head>
    {% block head %}
        {% include "partials/content_type.html.tpl" %}
        {% include "partials/includes.html.tpl" %}
        <title>Pingu / {% block title %}{% endblock %}</title>
    {% endblock %}
</head>
<body class="ux wait-load">
    {% include "partials/nav_data.html.tpl" %}
    <div id="overlay" class="overlay"></div>
    <div id="header">
        {% block header %}
            <h1>{% block name %}{% endblock %}</h1>
            <div class="links">
                {% if acl("index") %}
                    {% if link == "home" %}
                        <a href="{{ url_for('index') }}" class="active">home</a>
                    {% else %}
                        <a href="{{ url_for('index') }}">home</a>
                    {% endif %}
                {% endif %}
                {% if acl("servers.list") %}
                    //
                    {% if link == "servers" %}
                        <a href="{{ url_for('list_servers') }}" class="active">servers</a>
                    {% else %}
                        <a href="{{ url_for('list_servers') }}">servers</a>
                    {% endif %}
                {% endif %}
                {% if acl("contacts.list") %}
                    //
                    {% if link == "contacts" %}
                        <a href="{{ url_for('list_contacts') }}" class="active">contacts</a>
                    {% else %}
                        <a href="{{ url_for('list_contacts') }}">contacts</a>
                    {% endif %}
                {% endif %}
                {% if acl("accounts.list") %}
                    //
                    {% if link == "accounts" %}
                        <a href="{{ url_for('list_accounts') }}" class="active">accounts</a>
                    {% else %}
                        <a href="{{ url_for('list_accounts') }}">accounts</a>
                    {% endif %}
                {% endif %}
                {% if acl("about") %}
                    //
                    {% if link == "about" %}
                        <a href="{{ url_for('about') }}" class="active">about</a>
                    {% else %}
                        <a href="{{ url_for('about') }}">about</a>
                    {% endif %}
                {% endif %}
            </div>
        {% endblock %}
    </div>
    <div id="content">{% block content %}{% endblock %}</div>
    {% include "partials/footer.html.tpl" %}
</body>
{% include "partials/end_doctype.html.tpl" %}
