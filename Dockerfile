# Dockerfile

FROM python:3.10-slim

# Install system dependencies required for MetaTrader5, NumPy, and Pandas to build successfully
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
