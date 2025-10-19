# Dockerfile

FROM python:3.10

# إضافة متغير بيئة عشوائي لتجاوز الـ Cache بشكل إجباري
ARG CACHE_BREAKER=1

WORKDIR /app

# 1. تحديث pip
RUN pip install --upgrade pip

# 2. تثبيت المكتبات
COPY requirements.txt .
# استخدام الأمر --no-cache-dir و `--force-reinstall` لضمان تثبيت نظيف
RUN pip install --no-cache-dir --force-reinstall -r requirements.txt

# 3. نسخ باقي ملفات المشروع
COPY . .

# أمر التشغيل
CMD ["python", "main.py"]
