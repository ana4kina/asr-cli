FROM python:3.11

RUN apt-get update -y && \
        apt-get install -y \
        sox \
        libsox-dev \
        libsox-fmt-all \
        libsndfile1

WORKDIR /app
COPY . /app

RUN python3 -m pip install -e .
