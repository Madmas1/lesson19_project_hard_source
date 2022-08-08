import calendar
import datetime
import jwt

from flask import request, abort

from constants import JWT_ALGO, JWT_SECRET
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=True):
        user = self.user_service.get_by_username(username)

        if not user:
            return False

        if not is_refresh:
            if not self.user_service.compare_passwords(password, user.password):
                return False

        data = {
            "username": user.username,
            "user_role": user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        days90 = datetime.datetime.utcnow() + datetime.timedelta(days=90)
        data['exp'] = calendar.timegm(days90.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGO])
        username = data['username']
        user = self.user_service.get_by_username(username)

        if not user:
            return False

        return self.generate_tokens(username, user.password, is_refresh=True)


