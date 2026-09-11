FROM python:3.12.14-slim-bookworm

LABEL org.opencontainers.image.source="https://github.com/TokhirjonYuldoshev/my-docker-project"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY --chown=nobody:nogroup app.py .

USER nobody

CMD ["python", "app.py"]
