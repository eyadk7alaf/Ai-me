# Dockerfile

FROM python:3.10-slim

# تحديث حزم النظام وتثبيت حزم البناء الأساسية المطلوبة لـ MetaTrader5 و NumPy/Pandas
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# تثبيت متطلبات بايثون
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
