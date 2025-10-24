# syntax=docker/dockerfile:1.7
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

RUN useradd appuser
USER appuser
