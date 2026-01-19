FROM python:3.10-slim

WORKDIR /app

# 1. System dependencies (rarely changes)
RUN apt-get update && \
    apt-get install -y --no-install-recommends socat && \
    rm -rf /var/lib/apt/lists/*

# 2. Install uv
RUN pip install --no-cache-dir uv

# 3. Dependency files (invalidated only when deps change)
COPY pyproject.toml ./
COPY uv.lock ./
COPY ./blabot blabot/

# 4. Install dependencies
RUN uv sync

# 5. Cleanup
RUN rm -rf blabot/ pyproject.toml uv.lock

# 6. App code (changes frequently) - copied last
COPY ./examples/example_app.py ./
