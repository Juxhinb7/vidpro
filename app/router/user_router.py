from fastapi import APIRouter

from app.controller.user_controller import user_controller

user_router = APIRouter(prefix="/users", tags=["Users"])
user_router.add_api_route("/", user_controller.get_users, methods=["GET"])
