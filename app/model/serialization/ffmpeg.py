from pydantic import BaseModel


class FFMPEGVersionResponse(BaseModel):
    ffmpeg_version: str