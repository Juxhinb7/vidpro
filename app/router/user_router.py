from fastapi import APIRouter
from fastapi.params import Depends

from app.controller.user_controller import UserController
from app.model.serialization.action import ActionResponse
from app.model.serialization.user import User
from app.utility.auth_dependency import auth_dependency

user_router = APIRouter(prefix="/users", tags=["Users"])
user_router.add_api_route("/", UserController.read_users, methods=["GET"], response_model=list[User], dependencies=[Depends(auth_dependency)])
user_router.add_api_route("/user_profile", UserController.get_user_profile, methods=["GET"], dependencies=[Depends(auth_dependency)])
user_router.add_api_route("/create", UserController.register_user, methods=["POST"], status_code=201, response_model=ActionResponse)
user_router.add_api_route("/login", UserController.login_user, methods=["POST"], status_code=200, response_model=ActionResponse)
user_router.add_api_route("/logout", UserController.logout, methods=["POST"], status_code=200, response_model=ActionResponse, dependencies=[Depends(auth_dependency)])
user_router.add_api_route("/remove/{user_id}", UserController.remove_user, status_code=204, methods=["DELETE"])
