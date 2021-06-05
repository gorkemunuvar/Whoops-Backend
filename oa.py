from flask import g
from flask_oauthlib.client import OAuth
from oauthlib.common import Request

GOOGLE_APP_ID = '167345546409-et21u2i0r2cksg5avc563bjrd8ptvj60.apps.googleusercontent.com'
GOOGLE_APP_SECRET = 'o0oscaAYrGPPbASVNLcHrSqc'

FACEBOOK_APP_ID = '523200682045074'
FACEBOOK_APP_SECRET = 'b21043ce06dcae9df8ff9e4294d60381'

TWITTER_APP_ID = 'z1ZE4AUQe2NRIquxQndZvg81E'
TWITTER_APP_SECRET = 'aKXfHdCZkjIM8dVCt3n2Ptw2KgkwZicmrtVRWAOLk9oKws5V22'

# It is the link between the settings and our app
oauth = OAuth()

google = oauth.remote_app(
    'google',
    consumer_key=GOOGLE_APP_ID,
    consumer_secret=GOOGLE_APP_SECRET,
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


facebook = oauth.remote_app(
    'facebook',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    access_token_method='GET',
    authorize_url='https://www.facebook.com/dialog/oauth'
)

twitter = oauth.remote_app(
    'twitter',
    consumer_key=TWITTER_APP_ID,
    consumer_secret=TWITTER_APP_SECRET,
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize'
)


@google.tokengetter
def get_google_oauth_token():
    if 'access_token' in g:
        return g.access_token


@facebook.tokengetter
def get_facebook_oauth_token():
    if 'access_token' in g:
        return g.access_token


@twitter.tokengetter
def get_twitter_oauth_token():
    if 'access_token' in g:
        return g.access_token


""" 

    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']
 """
