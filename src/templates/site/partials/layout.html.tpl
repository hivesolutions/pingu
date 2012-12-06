{% include "site/partials/doctype.html.tpl" %}
<head>
    {% block head %}
        {% include "site/partials/content_type.html.tpl" %}
        {% include "site/partials/includes.html.tpl" %}
        <title>Pingu</title>
    {% endblock %}
</head>
<body class="ux wait-load">
    <div id="overlay" class="overlay"></div>
    <div id="header">
        {% block header %}
        {% endblock %}
    </div>
    <div id="content">{% block content %}{% endblock %}</div>
</body>
{% include "site/partials/end_doctype.html.tpl" %}
