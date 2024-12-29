FROM python:3.10-slim

WORKDIR /app

COPY ./examples/example.py ./

RUN apt-get update && \
    apt-get install -y --no-install-recommends socat && \
    rm -rf /var/lib/apt/lists/*

COPY ./blabot blabot/
COPY pyproject.toml ./

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    pip install --no-cache-dir . && \
    poetry install --no-root

RUN rm -rf blabot/ pyproject.toml poetry.lock
