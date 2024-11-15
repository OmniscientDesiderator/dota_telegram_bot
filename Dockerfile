FROM python:3.13.0-slim-bullseye

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY /app .

CMD ["python", "run.py"]