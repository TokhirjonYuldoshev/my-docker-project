FROM python:3.9-slim
COPY app.py /app.py
CMD ["python", "/app.py"]