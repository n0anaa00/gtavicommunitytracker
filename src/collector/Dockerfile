FROM python:3.9-slim

WORKDIR /app/collector

COPY src/collector/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/collector/ .

RUN mkdir -p /app/processor/input 

CMD ["python", "main.py"]