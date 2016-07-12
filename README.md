# highnoon

Simulates the typical Overwatch experience [playing against McCree](http://docs.highnoon.apiary.io/)

## How to Play

> Win by eliminating McCree before he defeats you

- Create a Player account and join a Game

- Choose an action: `pursue`, `retreat` or `showdown` in each round against McCree

- McCree takes his action *after* yours

- Based on your choices, McCree will take damage or gain progress towards High Noon

> McCree starts with 200 health and takes between `20 to 30` damage per successful attack

### The Choice

Each choice is strong against one of McCree's choices:

- Pursuing while he Retreats
- Retreating while he is in Showdown
- Showdown while he Pursues

If both you and McCree make the same choice, the round ends in a stalemate

### High Noon

Each round, McCree will gain an amount of progress towards triggering his ultimate ability `High Noon`

> If McCree chooses a strong choice against you, he gains more progress

When High Noon is used, is has a chance of instantly defeating you

> In later rounds the odds of losing to High Noon become more likely

Since McCree takes his action after yours, you can defeat him at the last second if his health is low and you damage him before he's able to trigger `High Noon`

## Building the App
1. Download the [google-python sdk](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)
2. Install to your local librarie path `unzip -d /usr/local/lib/python2.7/dist-packages/google_appengine google_appengine.zip`
3. Add library path to system path `export PATH=$PATH:/usr/local/lib/python2.7/dist-packages/google_appengine`
4. (optional) add the previous command to your `~/.bashrc` to persist across logins


### Deploying the app locally

1.  Run the app locally with `dev_appserver.py $app_folder`
1.  Test by visiting the [API Explorer on your local box](https://localhost:8080/_ah/api/explorer`)
2.  (optional) make `curl` requests to API endpoints at localhost

 
### Deploying the app on Google AppEngine

1.  Create a new application ID in [app-engine](https://console.cloud.google.com)
1.  Set `application` in app.yaml to the app ID you registered above
2.  Deploy to AppEngine using `appcfg.py update $app_folder`
> note: include the `--noauth_local_webserver` flag to authenticate from a headless box
> note: account credentials will be saved by default to `~/.appcfg_oauth2_tokens` - delete this file to be re-prompted to login as a different account
3. (optional) View and test endpoints at `$appname-appspot.com/_ah/api/explorer` 

> “Shall there be truth between us? 
> Not as friends, but as enemies and equals?” ― Stephen King, The Gunslinger
