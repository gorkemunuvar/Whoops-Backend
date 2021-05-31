import os
from flask import g
from flask_oauthlib.client import OAuth
from oauthlib.common import Request

# It is the link between the settings and our app
oauth = OAuth()

google = oauth.remote_app(
    'google',
    consumer_key='167345546409-et21u2i0r2cksg5avc563bjrd8ptvj60.apps.googleusercontent.com',
    consumer_secret='o0oscaAYrGPPbASVNLcHrSqc',
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@google.tokengetter
def get_google_oauth_token():
    if 'access_token' in g:
        return g.access_token
