# Dockerfile

# استخدام صورة بايثون القياسية (تتضمن حزم النظام الضرورية)
FROM python:3.10

WORKDIR /app

# الخطوة الحاسمة: تحديث pip أولاً لضمان عدم وجود أخطاء "exit code 1"
RUN pip install --upgrade pip

# نسخ ملف متطلبات المكتبات
COPY requirements.txt .

# تثبيت متطلبات بايثون
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع (وهي الآن منظمة بشكل صحيح)
COPY . .

# تحديد الأمر الذي سيتم تنفيذه عند تشغيل البوت
CMD ["python", "main.py"]
