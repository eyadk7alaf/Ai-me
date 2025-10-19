# Dockerfile

FROM python:3.10

WORKDIR /app

# الخطوة الجديدة والحاسمة: تحديث pip
RUN pip install --upgrade pip

COPY requirements.txt .

# تثبيت متطلبات بايثون
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
