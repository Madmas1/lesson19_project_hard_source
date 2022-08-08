import jwt
from flask import request, abort

from constants import JWT_SECRET, JWT_ALGO


def auth_required(func):
    def wrapper(*args, **kwargs):
        if not "Authorization" in request.headers:
            abort(401)

        token = request.headers["Authorization"]

        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        except Exception as error:
            print(f"JWT decode error:{error}")
            abort(401)
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if not "Authorization" in request.headers:
            abort(401)

        token = request.headers["Authorization"]

        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        except Exception as error:
            print(f"JWT decode error:{error}")
            abort(401)
            if data["role"] == "admin":
                return func(*args, **kwargs)
            else:
                abort(401)

        return func(*args, **kwargs)

    return wrapper
