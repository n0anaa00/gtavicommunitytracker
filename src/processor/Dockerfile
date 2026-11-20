FROM python:3.9-slim

WORKDIR /app/processor

COPY src/processor/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/processor/ .

CMD ["python", "main.py"]