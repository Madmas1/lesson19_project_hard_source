import base64
import hashlib
import hmac

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS

from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def create(self, user_data):
        user_data['password'] = self.get_hash(user_data['password'])
        return self.dao.create(user_data)

    def update(self, user_data):
        user_data['password'] = self.get_hash(user_data['password'])
        self.dao.update(user_data)

    def update_partial(self, user_data):
        uid = user_data.get("id")
        user = self.dao.get_one(uid)
        
        if "username" in user_data:
            user.username = user_data.get("username")
        if "password" in user_data:
            user.password = self.get_hash(user_data.get("password"))
        if "role" in user_data:
            user.role = user_data.get("trailer")

    def delete(self, uid):
        self.dao.delete(uid)

    def get_hash(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('-utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    def compare_passwords(self, hash_psw, psw):
        return hmac.compare_digest(base64.b64decode(hash_psw), base64.b64decode(self.get_hash(psw)))


