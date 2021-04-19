from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(self):
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id, fresh=False)

        return {"access_token": new_access_token}, 200
