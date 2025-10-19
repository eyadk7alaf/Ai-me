# Dockerfile

# استخدام صورة بايثون مستقرة تعتمد على Debian/Buster
FROM python:3.10-slim-buster

# تحديث حزم النظام قبل تثبيت بايثون (حاسم لحل مشاكل التبعيات)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# إضافة متغير عشوائي لتجاوز الـ Cache بشكل إجباري
ARG CACHE_BREAKER=2

# 1. تحديث pip
RUN pip install --upgrade pip

# 2. تثبيت المكتبات (باستخدام force-reinstall لضمان تثبيت نظيف)
COPY requirements.txt .
RUN pip install --no-cache-dir --force-reinstall -r requirements.txt

# 3. نسخ باقي ملفات المشروع
COPY . .

# تعيين منفذ التشغيل (مطلب أساسي لـ Flask/Railway)
ENV PORT 5000

# أمر التشغيل: تشغيل تطبيق الويب الجديد
CMD ["python", "app.py"]
