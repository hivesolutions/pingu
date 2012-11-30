[Pingu](http://addons.heroku.com/pingu) makes sure your applications don't sleep on the job.

Adding pingu to you application will make it be checked constantly for being awake and how
well it's performing (latency).

## Installing the Pingu add-on

To use Ranger on Heroku, install the addon:

    $ heroku addons:add pingu

Once Pingu has been added a `PINGU_APP_ID` setting will be available in the app configuration and will contain the
[[variable purpose, i.e. "canonical URL used to access the newly provisioned Pingu service instance."]].
This can be confirmed using the `heroku config:get` command.

After installing Pingu the application should be configured to fully integrate with the add-on.

## Troubleshooting

If it seems pingu is having sme problems please talk with us at support@pinguapp.com, we'll be more thant
happy to talk and solve the issue.

## Migrating between plans

<div class="note" markdown="1">Application owners should carefully manage the migration timing to ensure proper application function during the migration process.</div>

[[Specific migration process or any migration tips 'n tricks]]

Use the `heroku addons:upgrade` command to migrate to a new plan.

    $ heroku addons:upgrade pingu:newplan

## Removing the Pingu add-on

Pingu may be removed via the CLI. Note that any data stored in the server may become lost
and may not be recoverable.

    $ heroku addons:remove pingu

## Support

Additional information

Check out Pingu or email us at support@pinguapp.com.

All Pingu support and runtime issues should be submitted via on of the [Heroku Support channels](support-channels).
Any non-support related issues or product feedback is welcome at [[your channels]].
