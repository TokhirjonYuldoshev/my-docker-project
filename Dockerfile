FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY --chown=nobody:nogroup app.py .

USER nobody

CMD ["python", "app.py"]
