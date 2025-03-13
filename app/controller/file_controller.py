from datetime import datetime
from fastapi import UploadFile

import aiofiles
from starlette.background import BackgroundTasks

from globals import lock, PROGRESS


class FileController:
    @staticmethod
    async def upload_video(file: UploadFile, background_tasks: BackgroundTasks):
        file_bytes = await file.read()
        background_tasks.add_task(FileController.__write_to_file, file, file_bytes)

        return {"Result": "Upload started"}

    @staticmethod
    async def __write_to_file(file: UploadFile, file_bytes: bytes):
        sample = f"files/{file.filename}-{datetime.now()}.mp4"
        await lock.acquire()
        async with aiofiles.open(sample, "wb") as out_file:
            await out_file.write(file_bytes)
            PROGRESS["message"] = "Task done!"
        lock.release()



