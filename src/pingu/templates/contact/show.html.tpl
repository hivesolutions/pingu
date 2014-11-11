{% extends "partials/layout_contact.html.tpl" %}
{% block title %}Contacts{% endblock %}
{% block name %}{{ contact.name }}{% endblock %}
{% block content %}
    <div class="quote">{{ contact.email }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">phone</td>
                <td class="left value" width="50%">{{ contact.phone | default('-', true) }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">xmpp</td>
                <td class="left value" width="50%">{{ contact.xmpp | default('-', true) }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">twitter</td>
                <td class="left value" width="50%">
                    {% if contact.twitter %}
                        twitter.com/<a href="http://twitter.com/{{ contact.twitter }}">{{ contact.twitter }}</a>
                    {% else %}
                        -
                    {% endif %}
                </td>
            </tr>
            <tr>
                <td class="right label" width="50%">facebook</td>
                <td class="left value" width="50%">
                    {% if contact.facebook %}
                        facebook.com/<a href="http://facebook.com/{{ contact.facebook }}">{{ contact.facebook }}</a>
                    {% else %}
                        -
                    {% endif %}
                </td>
            </tr>
        </tbody>
    </table>
{% endblock %}
