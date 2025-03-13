from fastapi import  status
from fastapi.responses import JSONResponse

from app.service.ffmpeg_service import FFMPEGService


class FFMPEGController:
    @staticmethod
    async def get_ffmpeg_version():
        """
        Handler that outputs the ffmpeg version.
        """
        ffmpeg_version = await FFMPEGService.try_get_ffmpeg_version()

        return JSONResponse(status_code=status.HTTP_200_OK, content={"ffmpeg_version": ffmpeg_version})