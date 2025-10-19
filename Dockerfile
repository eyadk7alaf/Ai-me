# Dockerfile

# نستخدم الصورة القياسية لتجنب مشاكل حزم النظام
FROM python:3.10

WORKDIR /app

# 1. تحديث pip إلى أحدث نسخة (يحل مشكلة "exit code: 1")
RUN pip install --upgrade pip

# 2. نسخ ملف المتطلبات
COPY requirements.txt .

# 3. تثبيت المتطلبات (يجب أن يعمل الآن)
RUN pip install --no-cache-dir -r requirements.txt

# 4. نسخ باقي ملفات المشروع (وهي الآن منظمة بشكل صحيح)
COPY . .

# 5. أمر التشغيل
CMD ["python", "main.py"]
