[Pingu](http://addons.heroku.com/pingu) is an [add-on](http://addons.heroku.com) for providing functionality X.

Adding functionality X to an application provides benefits X, Y and Z. [[Sell the benefits here! Don't skimp - developers have many options these days.]]

Pingu is accessible via an API and has supported client libraries for [[Java|Ruby|Python|Node.js|Clojure|Scala]]*.

## Installing the Pingu add-on

To use Ranger on Heroku, install the addon:

    $ heroku addons:add pingu

Once Pingu has been added a `PINGU_APP_ID` setting will be available in the app configuration and will contain the
[[variable purpose, i.e. "canonical URL used to access the newly provisioned Pingu service instance."]].
This can be confirmed using the `heroku config:get` command.

After installing Pingu the application should be configured to fully integrate with the add-on.

## Troubleshooting

If [[feature X]] does not seem to be [[common issue Y]] then 
[[add specific commands to look for symptoms of common issue Y]].

## Migrating between plans

<div class="note" markdown="1">Application owners should carefully manage the migration timing to ensure proper application function during the migration process.</div>

[[Specific migration process or any migration tips 'n tricks]]

Use the `heroku addons:upgrade` command to migrate to a new plan.

    :::term
    $ heroku addons:upgrade pingu:newplan
    -----> Upgrading pingu:newplan to sharp-mountain-4005... done, v18 ($49/mo)
           Your plan has been updated to: pingu:newplan

## Removing the add-on

Pingu can be removed via the  CLI.

<div class="warning" markdown="1">This will destroy all associated data and cannot be undone!</div>

    :::term
    $ heroku addons:remove pingu
    -----> Removing pingu from sharp-mountain-4005... done, v20 (free)

Before removing Pingu a data export can be performed by [[describe steps if export is available]].

## Support

All Pingu support and runtime issues should be submitted via on of the [Heroku Support channels](support-channels). Any non-support related issues or product feedback is welcome at [[your channels]].