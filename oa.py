import os
from flask_oauthlib.client import OAuth
from oauthlib.common import Request

# It is the link between the settings and our app
oauth = OAuth()

github = oauth.remote_app(
    'github',
    consumer_key=os.getenv('GITHUB_CONSUMER_KEY'),
    consumer_secret=os.getenv('GITHUB_CONSUMER_SECRET'),
    # &scope=user:email
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
)

