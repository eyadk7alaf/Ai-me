# Dockerfile

# استخدام صورة بايثون رسمية (slim)
FROM python:3.10-slim

# الأمر الحاسم: تثبيت حزم النظام المطلوبة للبناء (يحل مشكلة "No matching distribution")
# build-essential و gcc ضروريان لبناء مكتبات مثل MetaTrader5 و Pandas
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

# نسخ باقي ملفات المشروع (يشمل ملفاتك المنظمة الآن)
COPY . .

# تحديد الأمر الذي سيتم تنفيذه عند تشغيل البوت
CMD ["python", "main.py"]
