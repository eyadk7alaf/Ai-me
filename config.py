import os
from dotenv import load_dotenv

load_dotenv() 

# ====================
# إعدادات MetaAPI الجديدة
# ====================
METAAPI_TOKEN = os.getenv('METAAPI_TOKEN', 'YOUR_METAAPI_TOKEN_HERE')
METAAPI_ACCOUNT_ID = os.getenv('METAAPI_ACCOUNT_ID', 'YOUR_METAAPI_ACCOUNT_ID_HERE')

# ====================
# إعدادات التليجرام
# ====================
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
ADMIN_TELEGRAM_ID = int(os.getenv('ADMIN_TELEGRAM_ID', '0'))
START_MESSAGE = "مرحباً! أنا بوت تداول آلي آمن. أرسل /admin للدخول للوحة التحكم."

# ====================
# إعدادات التداول والاستراتيجية
# ====================
TRADING_SYMBOLS = ['XAUUSD', 'EURUSD'] 
TIMEFRAMES = {
    'H4': 'H4',
    'H1': 'H1',
    'M15': 'M15'
}
RISK_PERCENT_PER_TRADE = 1.0
MAX_LOT_SIZE = 0.10
MIN_LOT_SIZE = 0.01 
