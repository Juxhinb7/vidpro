from fastapi import Request
from app.exception.auth_exception import AuthException
from app.utility.jwt_utility import JWTUtility


def auth_dependency(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise AuthException(message="You are not authorized to process this resource")

    payload = JWTUtility.verify_token(token)
    request.state.user = payload["sub"]

    return payload