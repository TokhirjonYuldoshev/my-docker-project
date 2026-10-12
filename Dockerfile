FROM python:3.12.15-slim-bookworm@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258

LABEL org.opencontainers.image.source="https://github.com/TokhirjonYuldoshev/my-docker-project"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY --chown=nobody:nogroup app.py .

USER nobody

CMD ["python", "app.py"]
