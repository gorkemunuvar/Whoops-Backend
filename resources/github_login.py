from flask_restful import Resource
from oa import github

class GithubLogin(Resource):
    @classmethod
    def get(cls):
        # Where we wanna go once the user authorized
        return github.authorize(callback='https://localhost:5000/login/github/authorized')