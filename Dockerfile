# Use an official Python image
FROM python:3.11

RUN apt update && apt install -y ffmpeg


COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN -p 6379:6379 --name redis_service -d redis

CMD ["fastapi", "run", "main.py"]
