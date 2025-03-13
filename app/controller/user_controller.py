from fastapi import Request, status
from fastapi.responses import Response

from starlette.responses import JSONResponse

from app.model.serialization.action import ActionResponse
from app.model.deserialization.user import User
from app.service.user_service import UserService

from app.utility.jwt_utility import JWTUtility
from werkzeug.security import generate_password_hash, check_password_hash


class UserController:
    @staticmethod
    async def read_users():
        """
        Returns list of users.
        """
        users = await UserService.get_users()
        return users

    @staticmethod
    async def get_user_profile(request: Request):
        user_info = request.state.user
        return {"message": "User profile", "user": user_info}

    @staticmethod
    async def register_user(user: User):
        """
        Handler that registers a user
        """

        # Verifies if user already exists. If it does, it returns a json response with an error message and a status code of 400 Bad Request.
        if await UserService.user_exists(user.username, user.email):
            action_response = ActionResponse(message="User already exists.").model_dump()
            return JSONResponse(status_code=400, content=action_response)

        # It gets a hashed password
        hashed_password = UserController.__get_hashed_password(user.password)

        # It creates a new user
        await UserService.create_user(user.username, user.email, hashed_password)

        action_response = ActionResponse(message="User created").model_dump()
        return JSONResponse(status_code=201, content=action_response)

    @staticmethod
    async def login_user(user: User):

        """
        Handler to login a user
        """

        user_data = await UserService.get_user(user.username, user.email)
        if not user_data:
            return JSONResponse(status_code=401, content={"message": "Incorrect username or email"})

        if not UserController.__verify_password(user.password, user_data["password"]):
            return JSONResponse(status_code=401, content={"message": "Incorrect password"})

        # Generate JWT Token
        access_token = JWTUtility.create_access_token(data={"sub": user_data["email"]})

        response = JSONResponse(status_code=200, content=ActionResponse(message="Login successful").model_dump())

        response.set_cookie(key="access_token", value=access_token, httponly=True, secure=False, samesite="strict")

        return response

    @staticmethod
    async def logout():
        response = JSONResponse(status_code=status.HTTP_200_OK, content=ActionResponse(message="Logout successful").model_dump())
        response.delete_cookie(key="access_token")
        return response

    @staticmethod
    async def remove_user(user_id):
        """
        Handler that removes a user
        """
        await UserService.remove_user(user_id)

        # returns 204 No Content Response for deleting a resource successfully
        return Response(status_code=204)

    @staticmethod
    def __get_hashed_password(password: str) -> str:
        """
        Responsible for hashing passwords
        """
        return generate_password_hash(password, method="scrypt")

    @staticmethod
    def __verify_password(plain_password: str, hashed_password: str) -> bool:
        return check_password_hash(hashed_password, plain_password)

