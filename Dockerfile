# Dockerfile

FROM python:3.10-slim

# تثبيت حزم النظام المطلوبة للبناء
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# تثبيت متطلبات بايثون
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
