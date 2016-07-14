# highnoon

Simulates the typical Overwatch experience - try to eliminate McCree before he takes out your entire team

## How to Play

> See the [endpoint documentation](http://docs.highnoon.apiary.io/) for details on request format and fields

- Create a Player account with a POST to `/player/new`  which returns your `player_id`
 
- Join a game with a POST to `/game/new` which returns a `game_id`

> Check the status of a game with a GET to `/game/status/$game_id`

> Check the status of a game with a GET to `/game/list/$player_id`

- Start the game by taking an action with a POST to `/game/play`: `pursue`, `retreat` or `showdown` 

> McCree takes his action *after* yours

- Based on your choices, McCree will take damage or gain progress towards High Noon

> McCree starts with 200 health and takes between `20 to 30` damage per successful attack

- Keep choosing actions for each round until one of you lies in the dust

> Keep an eye on the `hint` field in responses 

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

## Building the app
1. Download the [google-python sdk](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)
2. Install to your local path `unzip -d /usr/local/lib/python2.7/dist-packages/google_appengine google_appengine.zip`
3. Add library path to system path `export PATH=$PATH:/usr/local/lib/python2.7/dist-packages/google_appengine`
4. (optional) add the previous command to your `~/.bashrc` to persist across logins


### Deploying the app locally

1.  Run the app locally with `dev_appserver.py $app_folder`
1.  Test by visiting the [API Explorer on your local box](https://localhost:8080/_ah/api/explorer)
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
