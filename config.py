import os
from dotenv import load_dotenv

# يتم تحميل المتغيرات من ملف .env محليًا (لن يعمل على Railway، ولكنه مفيد للتجربة المحلية)
load_dotenv() 

# ====================
# إعدادات MT5
# ====================
# يتم تحويل المتغيرات إلى أنواعها الصحيحة (int/str) مع قيم افتراضية آمنة
MT5_LOGIN = int(os.getenv('MT5_LOGIN', '0'))
MT5_PASSWORD = os.getenv('MT5_PASSWORD', 'DEFAULT_PASS')
MT5_SERVER = os.getenv('MT5_SERVER', 'MetaQuotes-Demo')

# ====================
# إعدادات التليجرام
# ====================
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
ADMIN_TELEGRAM_ID = int(os.getenv('ADMIN_TELEGRAM_ID', '0'))
START_MESSAGE = "مرحباً! أنا بوت تداول آلي آمن. أرسل /admin للدخول للوحة التحكم."

# ====================
# إعدادات التداول والاستراتيجية
# ====================
TRADING_SYMBOLS = ['XAUUSD', 'EURUSD'] # الرموز التي سيتم تداولها
TIMEFRAMES = {
    'H4': 'H4',
    'H1': 'H1',
    'M15': 'M15'
}

# إدارة المخاطر
RISK_PERCENT_PER_TRADE = 1.0  # المخاطرة 1% لكل صفقة
MAX_LOT_SIZE = 0.10
MIN_LOT_SIZE = 0.01 
