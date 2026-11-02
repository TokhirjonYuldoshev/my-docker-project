FROM python:3.12.16-slim-bookworm@sha256:e697c81897302a4c4333bade000d98038fbb21eb064f8ee1fd42d02ebcd9d337

LABEL org.opencontainers.image.source="https://github.com/TokhirjonYuldoshev/my-docker-project"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY --chown=nobody:nogroup app.py .

USER nobody

CMD ["python", "app.py"]
