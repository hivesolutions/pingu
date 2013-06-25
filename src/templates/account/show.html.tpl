{% extends "partials/layout_account.html.tpl" %}
{% block title %}Accounts{% endblock %}
{% block name %}Accounts :: {{ account.username }}{% endblock %}
{% block content %}
    <div class="quote">{{ account.username }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">email</td>
                <td class="left value" width="50%">{{ account.email | default('-', true) }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">phone</td>
                <td class="left value" width="50%">{{ account.phone | default('-', true) }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">twitter</td>
                <td class="left value" width="50%">
                    {% if account.twitter %}
                        twitter.com/<a href="http://twitter.com/{{ account.twitter }}">{{ account.twitter }}</a>
                    {% else %}
                        -
                    {% endif %}
                </td>
            </tr>
            <tr>
                <td class="right label" width="50%">facebook</td>
                <td class="left value" width="50%">
                    {% if account.facebook %}
                        facebook.com/<a href="http://facebook.com/{{ account.facebook }}">{{ account.facebook }}</a>
                    {% else %}
                        -
                    {% endif %}
                </td>
            </tr>
        </tbody>
    </table>
{% endblock %}
