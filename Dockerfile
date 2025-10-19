# Dockerfile

# استخدام صورة بايثون رسمية (نوصي بـ 3.10 أو 3.11)
FROM python:3.10-slim

# تعيين دليل العمل
WORKDIR /app

# نسخ ملف متطلبات المكتبات
COPY requirements.txt .

# تثبيت متطلبات بايثون
# هذا السطر سيحل مشكلة تثبيت MetaTrader5 
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# تحديد الأمر الذي سيتم تنفيذه عند تشغيل الحاوية (البوت)
# عند النشر على Railway، سيتم تنفيذ الأمر التالي:
CMD ["python", "main.py"]
