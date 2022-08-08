from flask_restx import Resource, Namespace
from flask import request

from dao.model.user import UserSchema
from implemented import user_service
from service.decorators import admin_required, auth_required

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    @auth_required
    def get(self):
        rs = user_service.get_all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.get_json(force=True)
        user_service.create(req_json)
        return "The element was successfully added", 201


@user_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_required
    def get(self, uid):
        r = user_service.get_one(uid)
        us_d = UserSchema().dump(r)
        return us_d, 200

    @admin_required
    def put(self, bid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = bid
        user_service.update(req_json)
        return "", 204

    @admin_required
    def patch(self, uid: int):
        req_json = request.json
        req_json["id"] = uid
        user_service.update_partial(req_json)
        return "", 202

    @admin_required
    def delete(self, bid):
        user_service.delete(bid)
        return "", 204

