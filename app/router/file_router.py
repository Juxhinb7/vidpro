from fastapi import APIRouter
from fastapi.params import Depends

from app.controller.file_controller import FileController
from app.utility.auth_dependency import auth_dependency

file_router = APIRouter(prefix="/files", tags=["File handling"])
file_router.add_api_route(
    "/upload",
    FileController.upload_video,
    tags=["File Upload"],
    methods=["POST"],
    dependencies=[Depends(auth_dependency)]
)