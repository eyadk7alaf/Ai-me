# Dockerfile

# استخدام صورة بايثون رسمية (slim)
FROM python:3.10-slim

# تثبيت حزم النظام المطلوبة للبناء (ضرورية لمكتبات مثل pandas و MetaTrader5)
# هذه الخطوة تحل مشكلة "No matching dist"
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# تعيين دليل العمل
WORKDIR /app

# نسخ ملف متطلبات المكتبات
COPY requirements.txt .

# تثبيت متطلبات بايثون
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# تحديد الأمر الذي سيتم تنفيذه عند تشغيل البوت
CMD ["python", "main.py"]
