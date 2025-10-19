# Dockerfile

FROM python:3.10

WORKDIR /app

# تحديث pip
RUN pip install --upgrade pip

# نسخ ملف المتطلبات
COPY requirements.txt .

# تثبيت متطلبات بايثون الأخرى
RUN pip install --no-cache-dir -r requirements.txt

# تثبيت MetaTrader5 كخطوة منفصلة لتجاوز الـ Cache
# ملاحظة: نستخدم pip لتثبيته مباشرة هنا
RUN pip install MetaTrader5

# نسخ باقي ملفات المشروع
COPY . .

CMD ["python", "main.py"]
