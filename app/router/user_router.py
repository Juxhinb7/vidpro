from fastapi import APIRouter

from app.controller.user_controller import UserController

user_router = APIRouter(prefix="/users", tags=["Users"])
user_router.add_api_route("/", UserController.get_users, methods=["GET"])
