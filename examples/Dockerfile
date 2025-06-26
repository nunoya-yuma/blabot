FROM python:3.10-slim

WORKDIR /app

COPY ./examples/example_app.py ./

RUN apt-get update && \
    apt-get install -y --no-install-recommends socat && \
    rm -rf /var/lib/apt/lists/*

COPY ./blabot blabot/
COPY pyproject.toml ./
COPY uv.lock ./

RUN pip install --no-cache-dir uv && \
    uv sync

RUN rm -rf blabot/ pyproject.toml uv.lock
