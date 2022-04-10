FROM python:3.10-slim AS builder

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python-dev build-essential

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt


FROM python:3.10-slim

WORKDIR /app

# Env vars
ENV BOT_TOKEN ${BOT_TOKEN}

COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/* && \
    rm -rf /wheels && \
    addgroup --system app && adduser --system --group app

COPY --chown=app:app . /app

USER app

CMD ["python", "/app/bot.py"]
