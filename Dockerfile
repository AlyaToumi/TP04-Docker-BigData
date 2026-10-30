
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY analysis.py .

COPY data/ ./data/

CMD ["python", "analysis.py"]
