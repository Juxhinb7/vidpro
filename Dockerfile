# Use an official Python image
FROM python:3.11

RUN apt update && apt install -y ffmpeg

# Set the working directory
WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["fastapi", "run", "main.py"]