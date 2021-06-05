from symbol import parameters
from flask import request, g, url_for
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy import false

from oa import twitter
from models.user import UserModel


class TwitterLogin(Resource):
    @classmethod
    def get(cls):
        # Where we wanna go once the user authorized
        # return twitter.authorize(url_for('github.authorize', _external=True))
        return twitter.authorize(callback=url_for('twitter.authorized', _external=True, next=request.args.get('next')) or request.referrer or None)


class TwitterAuthorize(Resource):
    @classmethod
    def get(cls):
        resp = twitter.authorized_response()

        if resp is None:
            error_response = 'Access denied: reason=%s error=%s' % (
                request.args['error_reason'],
                request.args['error_description']
            )

            return error_response

        print(resp)
        twitter_token = resp['oauth_token']
        g.access_token = twitter_token

        parameters = {
            'Name': 'Example',
            'include_entities': False,
            'skip_status': True,
            'include_email': True
        }

        oauth_token = resp['oauth_token']
        oauth_token_secret = resp['oauth_token_secret']
        user_id = resp['user_id']
        screen_name = resp['screen_name']

        twitter_user = twitter.get(
            f'account/settings.json?oauth_token={oauth_token}&oauth_token_secret={oauth_token_secret}')

        """ twitter_user = twitter.get(
            f'account/verify_credentials?oauth_token={oauth_token}&oauth_token_secret={oauth_token_secret}&user_id={user_id}&screen_name={screen_name}&Name=Example&include_email=true',
        ) """

        #gmail = twitter_user.data['screen_name']

        # print(gmail)
        print(twitter_user.data)

        """ screen_name = resp['screen_name']
        print(f'User: {screen_name}')

        user = UserModel.find_by_email(screen_name)

        msg = ''
        if not user:
            user = UserModel(email=screen_name, password=None)
            user.save_to_db()
            msg = 'User created successfully and '

        access_token = create_access_token(
            identity=user.id,
            expires_delta=False,
            fresh=True
        )
        refresh_token = create_refresh_token(identity=user.id)

        return {
            "message": msg + "Logged in as {}".format(user.email),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, 200 """
