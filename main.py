import asyncio

from fastapi import FastAPI, WebSocket

from app.router.ffmpeg_router import ffmpeg_router
from app.router.file_router import file_router
from app.router.user_router import user_router
from app.utility.exception_handlers import register_exceptions
import logging
from globals import lock, PROGRESS

# Configure logging
logging.basicConfig(
    level=logging.ERROR,  # Set the logging level to ERROR
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', mode="w"),  # File handler that writes to app.log
        logging.StreamHandler()          # Stream handler that outputs to console
    ],
)

app = FastAPI()



register_exceptions(app)

app.include_router(user_router)
app.include_router(ffmpeg_router)
app.include_router(file_router)


@app.websocket("/ws")
async def progress_websocket(websocket: WebSocket):
    await websocket.accept()  # Accept the WebSocket connection

    try:
        while PROGRESS["message"] is None:
            await websocket.send_text("Waiting for message")
            await asyncio.sleep(1)



        await websocket.send_json({"message": PROGRESS["message"]})

    except Exception as e:
        print(f"Error: {e}")

    finally:
        await websocket.close()

