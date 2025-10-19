# Dockerfile

# استخدام صورة بايثون القياسية (تتضمن حزم النظام الضرورية)
FROM python:3.10

# تعيين دليل العمل
WORKDIR /app

# نسخ ملف متطلبات المكتبات
COPY requirements.txt .

# تثبيت متطلبات بايثون (هذا السطر لن يفشل الآن)
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع (وهي الآن منظمة بشكل صحيح في المجلدات)
COPY . .

# تحديد الأمر الذي سيتم تنفيذه عند تشغيل البوت
CMD ["python", "main.py"]
