FROM python:3.8-slim-buster
WORKDIR /app

COPY requirements.txt requirements.txt

ENV PYTHONUNBUFFERED 1

RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg

# really for ever file
# COPY ./main.py .
# COPY ./env.py .
COPY . .



CMD ["python3", "main.py"]

