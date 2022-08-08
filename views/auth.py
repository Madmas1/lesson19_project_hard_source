from flask_restx import Resource, Namespace
from flask import request, abort
from dao.model.director import DirectorSchema
from implemented import director_service, auth_service

auth_ns = Namespace('auth')


@auth_ns.route("/")
class AuthView(Resource):
    def post(self):
        req_json = request.get_json(force=True)
        username = req_json.get('username')
        password = req_json.get('password')
        if not (username or password):
            return "Need name and password", 400

        tokens = auth_service.generate_tokens(username, password)

        if tokens:
            return tokens
        else:
            return "Error request", 400
        # return tokens

    def put(self):
        req_json = request.get_json(force=True)
        ref_token = req_json.get('refresh_token')

        tokens = auth_service.approve_refresh_token(ref_token)

        if tokens:
            return tokens
        else:
            return "Error request", 400