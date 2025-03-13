# Use an official Python image
FROM python:3.11

RUN apt update && apt install -y ffmpeg


COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get install -y redis-server

EXPOSE 8000, 6379

CMD ["sh", "c", "redis-server --daemonize no && fastapi run main.py"]
