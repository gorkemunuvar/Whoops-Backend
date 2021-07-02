from flask import request, g, url_for
from flask_restful import Resource
from flask_oauthlib.client import OAuth, OAuthException
from flask_jwt_extended import create_access_token, create_refresh_token
from mongoengine import DoesNotExist

from oa import facebook
from models.user import User


class FacebookLogin(Resource):
    @classmethod
    def get(cls):
        # Where we wanna go once the user authorized
        # return facebook.authorize(url_for('github.authorize', _external=True))
        callback = url_for(
            'facebook.authorized',
            next=request.args.get('next') or request.referrer or None,
            _external=True
        )

        return facebook.authorize(callback=callback)


class FacebookAuthorize(Resource):
    @classmethod
    def get(cls):
        resp = facebook.authorized_response()

        if resp is None:
            error_response = 'Access denied: reason=%s error=%s' % (
                request.args['error_reason'],
                request.args['error_description']
            )

            return error_response

        if isinstance(resp, OAuthException):
            return 'Access denied: %s' % resp.message

        g.access_token = resp['access_token']
        facebook_user = facebook.get('/me?fields=name,email')

        mail = facebook_user.data['email']
        print(f'User: {mail}')

        msg = ''
        try:
            user = User.objects.get(email=mail)
        except DoesNotExist:
            user = User(email=mail, password=None)
            user.save()
            msg = 'User created successfully via Facebook OAuth.'


        access_token = create_access_token(
            identity=str(user.pk),
            expires_delta=False,
            fresh=True
        )
        refresh_token = create_refresh_token(identity=str(user.pk))

        print(msg)

        return {
            "message": msg + "Logged in as {}".format(user.email),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, 200
