from fastapi import APIRouter

from app.controller.ffmpeg_controller import FFMPEGController

ffmpeg_router = APIRouter(prefix="/ffmpeg-api", tags=["FFMPEG"])
ffmpeg_router.add_api_route("/ffmpeg-version", FFMPEGController.get_ffmpeg_version, methods=["GET"])