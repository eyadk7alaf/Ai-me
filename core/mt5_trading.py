import MetaTrader5 as mt5
import logging
import pandas as pd
from config import (
    MT5_LOGIN, MT5_PASSWORD, MT5_SERVER, 
    MAX_LOT_SIZE, MIN_LOT_SIZE, RISK_PERCENT_PER_TRADE
)

logger = logging.getLogger(__name__)

# ==================================
# 1. الاتصال بـ MT5
# ==================================

def initialize_mt5():
    """تهيئة الاتصال بمنصة MetaTrader 5."""
    if not mt5.initialize():
        logger.error(f"MT5 initialize() failed, error code = {mt5.last_error()}")
        return False
    
    # محاولة تسجيل الدخول
    if not mt5.login(MT5_LOGIN, MT5_PASSWORD, MT5_SERVER):
        logger.error(f"MT5 login failed! Account: {MT5_LOGIN}, Server: {MT5_SERVER}")
        # mt5.shutdown() # لا نغلقها إلا في نهاية البرنامج
        return False
    
    logger.info(f"MT5 connection successful for account: {MT5_LOGIN}")
    return True

# ==================================
# 2. إدارة المخاطر وحساب اللوت (0.01 - 0.10)
# ==================================

def calculate_lot_size(symbol: str, stop_loss_points: int):
    """
    حساب حجم العقد (Lot Size) بناءً على نسبة المخاطرة والرصيد.
    (stop_loss_points) هي المسافة بوحدات النقطة الداخلية لمنصة MT5.
    """
    
    account_info = mt5.account_info()
    symbol_info = mt5.symbol_info(symbol)
    
    if account_info is None or symbol_info is None:
        logger.warning("Could not get required info. Using minimum lot size.")
        return MIN_LOT_SIZE

    balance = account_info.balance
    
    # قيمة النقطة (Point Value) بالعملة الأساسية للحساب (عادة USD)
    tick_size = symbol_info.trade_tick_size
    tick_value = symbol_info.trade_tick_value
        
    # قيمة المخاطرة بالدولار (1% من الرصيد)
    risk_amount = balance * (RISK_PERCENT_PER_TRADE / 100)
    
    # حساب قيمة المخاطرة لكل لوت قياسي (1.00)
    # 1.00 lot risk per point = 10 units (for most pairs)
    risk_per_lot_unit = (stop_loss_points * tick_value) / tick_size 
    
    # حساب اللوت النظري
    if risk_per_lot_unit > 0:
        calculated_lot = risk_amount / risk_per_lot_unit
    else:
        calculated_lot = MIN_LOT_SIZE
    
    # تطبيق الحد الأدنى والأقصى للوت
    final_lot = max(MIN_LOT_SIZE, min(calculated_lot, MAX_LOT_SIZE))
    
    logger.info(f"Lot calculated for {symbol}: {final_lot:.2f} (Risk: {risk_amount:.2f}$)")
    return final_lot

# ==================================
# 3. تنفيذ الأوامر
# ==================================

def execute_trade(symbol: str, action: str, volume: float, sl_price: float, tp_price: float):
    """إرسال أمر التداول (شراء/بيع) إلى MT5."""
    
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        return False
        
    # الحصول على السعر (Ask للسراء، Bid للبيع)
    tick = mt5.symbol_info_tick(symbol)
    if action == "BUY":
        trade_type = mt5.ORDER_TYPE_BUY
        price = tick.ask
    elif action == "SELL":
        trade_type = mt5.ORDER_TYPE_SELL
        price = tick.bid
    else:
        return False
        
    # إعداد الطلب
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": trade_type,
        "price": price,
        "sl": sl_price,
        "tp": tp_price,
        "deviation": 10,  
        "magic": 202409, # رقم سحري لتحديد صفقات البوت
        "comment": "EA_Bot_Test",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }

    # إرسال الأمر
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logger.error(f"Order failed for {symbol}. Code: {result.retcode}. Comment: {result.comment}")
        return False
    
    logger.info(f"Order SUCCESSFUL! Type: {action}, Volume: {volume}, Result: {result.deal}")
    return True
