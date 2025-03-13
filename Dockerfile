# Use an official Python image
FROM python:3.11

RUN apt update && apt install -y ffmpeg

RUN apt install rabbitmq-server

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["fastapi run main.py && celery -A api.worker worker --loglevel=INFO"]