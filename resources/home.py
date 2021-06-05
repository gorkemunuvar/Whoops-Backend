from flask_restful import Resource


class HomePage(Resource):
    @classmethod
    def get(self):
        return {'message': 'Whoops Home Page'}, 200
