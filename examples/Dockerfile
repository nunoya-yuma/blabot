FROM python:3.10-slim

WORKDIR /app

COPY ./examples/example.py ./

RUN apt-get update && \
    apt-get install -y --no-install-recommends git socat && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
