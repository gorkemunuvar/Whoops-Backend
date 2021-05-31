from flask import request, g, url_for
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token

from oa import google
from models.user import UserModel


class GoogleLogin(Resource):
    @classmethod
    def get(cls):
        # Where we wanna go once the user authorized
        # return google.authorize(url_for('github.authorize', _external=True))
        return google.authorize(callback=url_for('google.authorized', _external=True))


class GoogleAuthorize(Resource):
    @classmethod
    def get(cls):
        resp = google.authorized_response()

        if resp is None:
            error_response = 'Access denied: reason=%s error=%s' % (
                request.args['error_reason'],
                request.args['error_description']
            )

            return error_response

        g.access_token = resp['access_token']
        google_user = google.get('userinfo')

        gmail = google_user.data['email']
        print(f'User: {gmail}')

        user = UserModel.find_by_email(gmail)

        msg = ''
        if not user:
            user = UserModel(email=gmail, password=None)
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
        }, 200
