{% extends "site/partials/layout.html.tpl" %}
{% block title %}Pingu{% endblock %}
{% block content %}
    <div class="window window-screenshots lightbox">
        <img class="screen" />
        <div class="button-bar">
            <span class="screen-index">2</span> of <span class="screen-counter">5</span>
            <div class="button previous-button"></div>
            <div class="button next-button"></div>
            <div class="button close-button"></div>
        </div>
        <ul class="screens">
            <li>{{ url_for("static", filename = "images/site/app-screenshot-dummy.png") }}</li>
            <li>{{ url_for("static", filename = "images/site/app-screenshot-dummy2.png") }}</li>
        </ul>
    </div>
    <div class="window window-signup">
        <div class="button close-button"></div>
        <form action="{{ url_for('create_account_json') }}" method="post" class="form form-ajax">
            <h1>Signup</h1>
            <div class="line">
                <div class="label">Username</div>
                <div class="field"><input name="username" type="text" class="text-field" /></div>
                <div class="clear"></div>
            </div>
            <div class="line">
                <div class="label">Email</div>
                <div class="field"><input name="email" type="text" class="text-field" /></div>
                <div class="clear"></div>
            </div>
            <div class="line">
                <div class="label">Confirm Email</div>
                <div class="field"><input name="email_confirm" type="text" class="text-field" /></div>
                <div class="clear"></div>
            </div>
            <div class="separator"></div>
            <div class="line">
                <div class="label">Password</div>
                <div class="field"><input name="password" type="password" class="text-field" /></div>
                <div class="clear"></div>
            </div>
            <div class="line">
                <div class="label">Confirm Password</div>
                <div class="field"><input name="password_confirm" type="password" class="text-field" /></div>
                <div class="clear"></div>
            </div>
            <div class="separator"></div>
            <div class="line">
                <div class="label">Plan</div>
                <div class="field">
                    <input name="plan" type="radio" id="basic" value="basic" checked="1" /><label for="basic">Basic</label>
                    <input name="plan" type="radio" id="advanced" value="advanced" /><label for="advanced">Advanced</label>
                </div>
                <div class="clear"></div>
            </div>
            <div class="terms">
                By clicking <strong>Signup</strong>, you agree to our <a href="#">Service Agreement</a>
                and that you have read and understand our <a href="#">Privacy Policy</a>.
            </div>
            <div class="button button-submit" data-submit="true">Signup</div>
            <div class="form-success">
                <h1>Confirmation</h1>
                <div class="confirmation">
                    <p>
                        You should have now received a <strong>confirmation email</strong> indicating
                        the next steps in order to enable you account (for now disabled).
                    </p>
                    <p>
                        If you believe an error has occured please
                        <a href="{{ url_for('resend', username = '') }}%[username]" class="link" data-ajax="1">resend email</a>
                        and verify you inbox again.
                    </p>
                </div>
            </div>
        </form>
    </div>
    <div class="section section-title">
        <div class="main-illustration"></div>
        <div class="main-text">
            <div class="main-logo"></div>
            <h1>Keeping all the balls juggling in the air</h1>
            <h2>a webserver performance & monitoring tool that helps
            you keep your server online at all times</h2>
        </div>
        <div class="clear"></div>
    </div>
    <div class="section section-features">
        <h1>Features</h1>
        <ul class="features features-left">
            <li class="public-profile">
                <h3>Public Profile</h3>
                <p>
                    Expose performance and uptime statistics
                    to the world
                </p>
            </li>
            <li class="email-notifications">
                <h3>Email Notifications</h3>
                <p>
                    Receive email notifications every time your
                    services go down
                </p>
            </li>
            <li class="iphone-android">
                <h3>iPhone & Android Apps</h3>
                <p>
                    Track the performance of your services anywhere,
                    at any time
                </p>
            </li>
            <li class="xmpp">
                <h3>XMPP</h3>
                <p>
                    Get downtime notifications through your favorite
                    chat clients
                </p>
            </li>
        </ul>
        <ul class="features features-right">
            <li class="web-interface">
                <h3>Web Interface</h3>
                <p>
                    Monitor and configure which services you want to
                    monitor
                </p>
            </li>
            <li class="sms-messages">
                <h3>SMS Messages</h3>
                <p>
                    Get immediate SMS notifications whenever your
                    servers go down
                </p>
            </li>
            <li class="rest-api">
                <h3>REST API</h3>
                <p>
                    Feed your service data to your apps with our
                    friendly API
                </p>
            </li>
            <li class="daily-reports">
                <h3>Daily Reports</h3>
                <p>
                    Learn how your services are behaving throughout
                    the day
                </p>
            </li>
        </ul>
        <div class="clear"></div>
        <div class="button check-screenshots button-screenshots" data-window_open=".window-screenshots"></div>
    </div>
    <div class="section section-pricing">
        <h1>Pricing</h1>
        <table>
            <thead>
                <tr>
                    <th data-width="240"></th>
                    <th data-width="200">Basic</th>
                    <th data-width="200">Advanced</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Web Interface</td>
                    <td class="marked"></td>
                    <td class="marked"></td>
                </tr>
                <tr>
                    <td>Email Notifications</td>
                    <td class="marked"></td>
                    <td class="marked"></td>
                </tr>
                <tr>
                    <td>Public Profile</td>
                    <td class="marked"></td>
                    <td class="marked"></td>
                </tr>
                <tr>
                    <td>SMS Messages</td>
                    <td>-</td>
                    <td>20 / month</td>
                </tr>
                <tr>
                    <td>Daily Reports</td>
                    <td class="unmarked"></td>
                    <td class="marked"></td>
                </tr>
                <tr>
                    <td>iPhone & Android Apps</td>
                    <td class="unmarked"></td>
                    <td class="marked"></td>
                </tr>
                <tr>
                    <td>REST API</td>
                    <td class="unmarked"></td>
                    <td class="marked"></td>
                </tr>
                <tr>
                    <td>XMPP</td>
                    <td class="unmarked"></td>
                    <td class="marked"></td>
                </tr>
                <tr>
                    <td>Servers Included</td>
                    <td>5 <sup class="superscript">*</sup></td>
                    <td>15 <sup class="superscript">*</sup></td>
                </tr>
                <tr>
                    <td>Average Ping Interval</td>
                    <td>10 min</td>
                    <td>2 min</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <td>* Price per extra server: USD 0,75/month</td>
                    <td class="price">
                        <span class="value">3</span>
                        <span class="currency">USD</span>
                        <div class="frequency">month</div>
                    </td>
                    <td class="price">
                        <span class="value">10</span>
                        <span class="currency">USD</span>
                        <div class="frequency">month</div>
                    </td>
                </tr>
            </tfoot>
        </table>
        <div class="trial-included"></div>
        <div class="button button-submit button-signup" data-window_open=".window-signup">Signup</div>
        <div class="available-on">
            <h4>available on</h4>
            <a href="#"><img src="{{ url_for('static', filename = 'images/site/available-heroku.png') }}" /></a>
            <a href="#"><img src="{{ url_for('static', filename = 'images/site/available-app_store.png') }}" /></a>
            <a href="#"><img src="{{ url_for('static', filename = 'images/site/available-google_play.png') }}" /></a>
        </div>
    </div>
{% endblock %}
