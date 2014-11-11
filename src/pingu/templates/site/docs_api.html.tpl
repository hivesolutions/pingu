{% extends "site/partials/layout.html.tpl" %}
{% block title %}API Documentation{% endblock %}
{% block content %}
    <div class="content-docs">
        <div class="header">
            <div class="logo-header button" data-link="{{ url_for('index') }}"></div>
            <div class="account-header">
                <h4>João Magalhães</h4>
            </div>
            <div class="clear"></div>
        </div>
        <div class="header-docs">
            <h1>API Documentation</h1>
            <div class="links-docs">
                <a href="#general">General</a>
                //
                <a href="#authentication">Authentication</a>
                //
                <a href="#server">Server</a>
                //
                <a href="#contacts">Contacts</a>
                //
                <a href="#account">Account</a>
            </div>
        </div>
        <p>
            The REST API is the underlying interface for all of our official Dropbox mobile apps and our SDKs.
            It's the most direct way to access the API. This reference document is designed for those interested
            in developing for platforms not supported by the SDKs or for those interested in exploring API
            features in detail.
        </p>
        <h2 id="general">General</h2>
        <h3>SSL only</h3>
        <p>
            We require that all requests are done over SSL.
        </p>
        <h3>App folder access type</h3>
        <p>
            The default root level access type, app folder (as described in <a hreF="https://www.dropbox.com/developers/start/core">core concepts</a>), is referenced
            in API URLs by its codename sandbox. This is the only place where such a distinction is made.
        </p>
        <h3>UTF-8 encoding</h3>
        <p>
            Every string passed to and from the Dropbox API needs to be UTF-8 encoded.
            For maximum compatibility, normalize to Unicode Normalization Form C (NFC)
            before UTF-8 encoding.
        </p>
        <h3>Version numbers</h3>
        <p>
            The current version of our API is version 1. Most version 0 methods will
            work for the time being, but some of its methods risk being removed (most
            notably, the version 0 API methods /token and /account).
        </p>
        <h2 id="authentication">Authentication</h2>
        <h2 class="method">/login</h2>
        <h2 class="method-type">GET</h2>
        <dl>
            <dt>Description</dt>
            <dd>
                Step 2 of authentication. Applications should direct the user to /oauth/authorize.
                This isn't an API call per se, but rather a web endpoint that lets the user sign in
                to Dropbox and choose whether to grant the application the ability to access files
                on their behalf. The page served by /oauth/authorize should be presented to the user
                through their web browser. Without the user's authorization in this step, it isn't
                possible for your application to obtain an access token from /oauth/access_token.
            </dd>
            <dt>Parameters</dt>
            <dd>
                <p>
                    <strong class="type">oauth_token</strong> required The request token obtained via /oauth/request_token.
                </p>
                <p>
                    <strong class="type">oauth_callback</strong> after the either decides to authorize or disallow your application,
                    they are redirected to this URL.
                </p>
                <p>
                    <strong class="type">locale</strong> if the locale specified is a supported language, Dropbox will direct
                    users to a translated version of the authorization website. See the notes above
                    for more information about supported locales.
                </p>
            </dd>
            <dt>Returns</dt>
            <dd>
                Because the application doesn't call /oauth/authorize directly, there is no direct
                return value. After the user authorizes the application, use its request token to
                retrieve an access token via the /oauth/access_token API call. If the oauth_callback
                parameter is omitted, the application must find some other way of determining when
                the authorization step is complete. For example, the application can have the user
                explicitly indicate to it that this step is complete, but this flow may be less
                intuitive for users than the redirect flow.

                If oauth_callback is specified and the user authorizes the application, they will
                get redirected to the specified URL with the following additional URL query
                parameters appended:

                oauth_token The request token that was just authorized. The request token secret isn't sent back.
                uid The user's unique Dropbox ID.

                If the user chooses not to authorize the application, they will get redirected to the
                oauth_callback URL with the additional URL query parameter not_approved=true.
            </dd>
        </dl>
        <h2 class="method">/logout</h2>
        <h2 class="method-type">GET</h2>
        <dl>
            <dt>Description</dt>
            <dd>
                Step 2 of authentication. Applications should direct the user to /oauth/authorize.
                This isn't an API call per se, but rather a web endpoint that lets the user sign in
                to Dropbox and choose whether to grant the application the ability to access files
                on their behalf. The page served by /oauth/authorize should be presented to the user
                through their web browser. Without the user's authorization in this step, it isn't
                possible for your application to obtain an access token from /oauth/access_token.
            </dd>
            <dt>Parameters</dt>
            <dd>
                <p>
                    <strong class="type">oauth_token</strong> required The request token obtained via /oauth/request_token.
                </p>
                <p>
                    <strong class="type">oauth_callback</strong> after the either decides to authorize or disallow your application,
                    they are redirected to this URL.
                </p>
                <p>
                    <strong class="type">locale</strong> if the locale specified is a supported language, Dropbox will direct
                    users to a translated version of the authorization website. See the notes above
                    for more information about supported locales.
                </p>
            </dd>
            <dt>Returns</dt>
            <dd>
                Because the application doesn't call /oauth/authorize directly, there is no direct
                return value. After the user authorizes the application, use its request token to
                retrieve an access token via the /oauth/access_token API call. If the oauth_callback
                parameter is omitted, the application must find some other way of determining when
                the authorization step is complete. For example, the application can have the user
                explicitly indicate to it that this step is complete, but this flow may be less
                intuitive for users than the redirect flow.

                If oauth_callback is specified and the user authorizes the application, they will
                get redirected to the specified URL with the following additional URL query
                parameters appended:

                oauth_token The request token that was just authorized. The request token secret isn't sent back.
                uid The user's unique Dropbox ID.

                If the user chooses not to authorize the application, they will get redirected to the
                oauth_callback URL with the additional URL query parameter not_approved=true.
            </dd>
        </dl>
        <h2 id="server">Server</h2>
        <h2 class="method">/servers</h2>
        <h2 class="method-type">POST</h2>
        <dl>
            <dt>Description</dt>
            <dd>
                Step 2 of authentication. Applications should direct the user to /oauth/authorize.
                This isn't an API call per se, but rather a web endpoint that lets the user sign in
                to Dropbox and choose whether to grant the application the ability to access files
                on their behalf. The page served by /oauth/authorize should be presented to the user
                through their web browser. Without the user's authorization in this step, it isn't
                possible for your application to obtain an access token from /oauth/access_token.
            </dd>
            <dt>Parameters</dt>
            <dd>
                <p>
                    <strong class="type">oauth_token</strong> required The request token obtained via /oauth/request_token.
                </p>
                <p>
                    <strong class="type">oauth_callback</strong> after the either decides to authorize or disallow your application,
                    they are redirected to this URL.
                </p>
                <p>
                    <strong class="type">locale</strong> if the locale specified is a supported language, Dropbox will direct
                    users to a translated version of the authorization website. See the notes above
                    for more information about supported locales.
                </p>
            </dd>
            <dt>Returns</dt>
            <dd>
                <p>
                    Because the application doesn't call /oauth/authorize directly, there is no direct
                    return value. After the user authorizes the application, use its request token to
                    retrieve an access token via the /oauth/access_token API call. If the oauth_callback
                    parameter is omitted, the application must find some other way of determining when
                    the authorization step is complete. For example, the application can have the user
                    explicitly indicate to it that this step is complete, but this flow may be less
                    intuitive for users than the redirect flow.
                </p>
                <p>
                    If oauth_callback is specified and the user authorizes the application, they will
                    get redirected to the specified URL with the following additional URL query
                    parameters appended:
                </p>
                <p>
                    <strong class="type">oauth_token</strong> The request token that was just authorized.
                    The request token secret isn't sent back.
                </p>
                <p>
                    <strong class="type">uid</strong> The user's unique Dropbox ID.
                </p>
                <p>
                    If the user chooses not to authorize the application, they will get redirected to the
                    oauth_callback URL with the additional URL query parameter not_approved=true.
                </p>
                <p>
                    Sample JSON response<br />
<pre>{
    "referral_link": "https://www.dropbox.com/referrals/",
    "display_name": "John P. User",
    "uid": 12345678,
    "country": "US",
    "quota_info": {
        "shared": 253738410565,
        "quota": 107374182400000,
        "normal": 680031877871
    }
}
</pre>
                </p>
            </dd>
            <h2 id="contacts">Contacts</h2>
            <h2 id="account">Account</h2>
        </dl>
    </div>
{% endblock %}
