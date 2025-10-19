import logging
import asyncio
# استيراد المكتبة الجديدة
from metaapi_cloud_sdk import MetaApi
from config import METAAPI_TOKEN, METAAPI_ACCOUNT_ID, RISK_PERCENT_PER_TRADE
from typing import Literal

logger = logging.getLogger(__name__)

# المتغير العام الذي سيحمل اتصال الحساب
ACCOUNT = None
API = None

# ==================================
# 1. الاتصال بـ MetaApi (async)
# ==================================

async def initialize_metaapi():
    """تهيئة الاتصال بخدمة MetaApi وربط الحساب."""
    global API, ACCOUNT
    
    if API and ACCOUNT:
        return True

    API = MetaApi(METAAPI_TOKEN)
    
    try:
        # البحث عن الحساب المحدد
        account_found = await API.get_account(METAAPI_ACCOUNT_ID)
        if not account_found:
            logger.error(f"FATAL ERROR: MetaApi account ID {METAAPI_ACCOUNT_ID} not found.")
            return False
        
        ACCOUNT = account_found
        
        # الانتظار حتى يصبح الحساب جاهزاً للتداول
        logger.info("Connecting to MetaApi account...")
        # تأكد من أن حسابك Deploy (منشور) على MetaApi قبل هذه الخطوة
        await ACCOUNT.wait_until_connected()
        
        # التأكد من أن التداول متاح
        if ACCOUNT.state != 'CONNECTED':
            logger.error(f"MetaApi account not connected, state: {ACCOUNT.state}")
            return False
            
        logger.info(f"MetaApi connection successful for account: {METAAPI_ACCOUNT_ID}")
        return True

    except Exception as e:
        logger.error(f"Failed to initialize MetaApi: {e}")
        return False

# ==================================
# 2. إدارة المخاطر وحساب اللوت (async)
# ==================================

async def calculate_lot_size(symbol: str, stop_loss_points: int):
    """حساب حجم العقد بناءً على نسبة المخاطرة والرصيد."""
    if not ACCOUNT:
        await initialize_metaapi()
    if not ACCOUNT:
        return 0.01

    try:
        account_information = await ACCOUNT.get_account_information()
        if not account_information:
            return 0.01

        balance = account_information['balance']
        
        symbol_spec = await ACCOUNT.get_specification(symbol)
        if not symbol_spec:
            return 0.01
            
        # قيمة النقطة (Pip Value)
        point_value = symbol_spec['pipValue'] 
        
        risk_amount = balance * (RISK_PERCENT_PER_TRADE / 100)
        risk_per_lot_unit = stop_loss_points * point_value
        
        if risk_per_lot_unit > 0:
            calculated_lot = risk_amount / risk_per_lot_unit
        else:
            calculated_lot = 0.01

        from config import MAX_LOT_SIZE, MIN_LOT_SIZE
        final_lot = max(MIN_LOT_SIZE, min(calculated_lot, MAX_LOT_SIZE))
        
        logger.info(f"Lot calculated for {symbol}: {final_lot:.2f}")
        return final_lot
    
    except Exception as e:
        logger.error(f"Error calculating lot size: {e}")
        return 0.01

# ==================================
# 3. تنفيذ الأوامر (async)
# ==================================

async def execute_trade(symbol: str, action: Literal["BUY", "SELL"], volume: float, sl_price: float, tp_price: float):
    """إرسال أمر التداول (شراء/بيع) إلى MetaApi."""
    
    if not ACCOUNT:
        logger.error("MetaApi account not initialized for trading.")
        return False
        
    try:
        # استخدام execute_market_order لإرسال الأمر
        result = await ACCOUNT.create_market_order(
            symbol=symbol,
            type=action.upper(),
            volume=volume,
            stopLoss=sl_price,
            takeProfit=tp_price,
            comment="EA_MetaApi_Bot"
        )

        logger.info(f"Order SUCCESSFUL! Type: {action}, Volume: {volume}, Result: {result}")
        return True
    
    except Exception as e:
        logger.error(f"Order failed for {symbol}: {e}")
        return False
        
# ==================================
# 4. دالة مساعدة لـ main.py (للتوافق)
# ==================================

def initialize_mt5():
    """هذه الدالة موجودة للتوافق مع main.py لكنها تشغل initialize_metaapi."""
    # نستخدم asyncio.run لتشغيل الدالة المزامنة initialize_metaapi
    try:
        asyncio.run(initialize_metaapi())
        return True
    except Exception as e:
        logger.error(f"FATAL ERROR: Could not run MetaApi initialization: {e}")
        return False
