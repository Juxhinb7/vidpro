from fastapi import FastAPI, Request, status
from jwt import ExpiredSignatureError, InvalidTokenError
from starlette.responses import JSONResponse

from app.exception.auth_exception import AuthException
from app.exception.cookie_exception import CookieException
from app.exception.user_exception import UserException
from app.model.serialization.action import ActionResponse

def register_exceptions(app: FastAPI):
    @app.exception_handler(Exception)
    def auth_exception_handler(_request: Request, exc: Exception):
        match exc:
            case AuthException() \
                 | UserException() \
                 | CookieException() \
                 | ExpiredSignatureError() \
                 | InvalidTokenError():
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=ActionResponse(message=str(exc)).model_dump())
