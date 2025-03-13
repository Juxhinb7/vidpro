from fastapi import APIRouter
from fastapi.params import Depends

from app.controller.ffmpeg_controller import FFMPEGController
from app.model.serialization.ffmpeg import FFMPEGVersionResponse
from app.utility.auth_dependency import auth_dependency

ffmpeg_router = APIRouter(tags=["FFMPEG"])
ffmpeg_router.add_api_route("/ffmpeg-version", FFMPEGController.get_ffmpeg_version, methods=["GET"], response_model=FFMPEGVersionResponse, dependencies=[Depends(auth_dependency)])