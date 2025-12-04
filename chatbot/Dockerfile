FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código y datasets
COPY app.py index.html ./
COPY data ./data
COPY assets ./assets 


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]