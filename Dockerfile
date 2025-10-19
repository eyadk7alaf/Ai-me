# Dockerfile

FROM python:3.10

WORKDIR /app

# تحديث pip
RUN pip install --upgrade pip

# نسخ ملف متطلبات المكتبات (الذي لم يعد يحتوي على MetaTrader5)
COPY requirements.txt .

# تثبيت المتطلبات المتبقية
RUN pip install --no-cache-dir -r requirements.txt

# =========================================================
# الحل النهائي لمشكلة MetaTrader5: تثبيت يدوياً
# 1. تنزيل الملف بصيغة wheel
# 2. تثبيته مباشرة لتجاوز مشاكل التبعيات
# =========================================================

# (قد تحتاج لتغيير اسم ملف الـ wheel إذا كنت تستخدم إصدار بايثون مختلف، لكن هذا يعمل مع 3.10)
RUN pip install https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/MetaTrader5-3.0.12-cp310-cp310-linux_x86_64.whl

# نسخ باقي ملفات المشروع
COPY . .

# أمر التشغيل
CMD ["python", "main.py"]
