# aceofblades

A card-game knife-fight with [two players and one winner](http://docs.aceofblades.apiary.io/)

> “Shall there be truth between us? 
> Not as friends, but as enemies and equals?” ― Stephen King, The Gunslinger


## Build instructions
1. Download the [google-python sdk](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)
2. Install to your local libraries `unzip -d /usr/local/lib/python2.7/dist-packages/google_appengine google_appengine.zip`
3. Add library path `export PATH=$PATH:/usr/local/lib/python2.7/dist-packages/google_appengine`
4. (optional) add the above path definition to your `~/.bashrc` to persist across logins
 
### dev

1.  Run the app locally with `dev_appserver.py $folder`
1.  Test by visiting the API Explorer - by default `localhost:8080/_ah/api/explorer`

 
### deploy

1.  Create a new application ID in [app-engine](https://console.cloud.google.com)
1.  Set `application` in app.yaml to the app ID you have registered
2.  Deploy to AppEngine using `appcfg.py -A $app_id`


## How to Play
Make queries to [public API endpoints](http://docs.aceofblades.apiary.io/#reference/0/starting-a-new-game) using your preferred client

