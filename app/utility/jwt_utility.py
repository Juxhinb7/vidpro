from typing import Optional
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Request
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer

from app.exception.cookie_exception import CookieException
from app.exception.user_exception import UserException
from app.service.user_service import UserService

from config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class JWTUtility:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        # Ensure the 'sub' field is part of the data dictionary (typically email)
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        # Add expiration time to the token and the 'sub' field (email or user id)
        to_encode.update({
            "exp": expire,
            "sub": to_encode.get("sub")  # This should be the email
        })

        # Encode the token using the secret key and the HS256 algorithm
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

def __get_jwt_token_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise CookieException(message="No token was found inside the cookie")

    return token


async def get_current_user(token: str = Depends(__get_jwt_token_from_cookie)):
    payload = JWTUtility.verify_token(token)

    email = payload.get("sub")
    user = await UserService.get_user_by_email(email)
    if user is None:
        raise UserException(message="User not found")
    return user