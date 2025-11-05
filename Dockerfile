# syntax=docker/dockerfile:1.7
FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.9.6 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd -m -d /home/appuser -s /bin/bash appuser 

WORKDIR /app
ENV UV_PROJECT_ENVIRONMENT=/home/appuser/.venv
ENV PATH="/home/appuser/.venv/bin:$PATH"
    
COPY uv.lock pyproject.toml ./

RUN mkdir -p /home/appuser/.cache/uv \
 && chown -R appuser:appuser /home/appuser /app
USER appuser

RUN uv sync --locked
