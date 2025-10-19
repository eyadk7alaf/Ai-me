import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.core_strategy import get_final_signal
from core.mt5_trading import execute_trade, calculate_lot_size
from config import TRADING_SYMBOLS

logger = logging.getLogger(__name__)

# ==================================
# الوظيفة الرئيسية لمراقبة التداول
# ==================================

async def trade_monitor():
    """
    الوظيفة الرئيسية التي تعمل بشكل متكرر (كل دقيقة).
    تقوم بفحص جميع الأزواج وإصدار أوامر التداول عند وجود إشارة قوية.
    """
    
    logger.info("--- Starting Trade Monitor Cycle ---")

    # نمر على كل رمز تداول محدد في config.py
    for symbol in TRADING_SYMBOLS:
        # 1. الحصول على الإشارة النهائية (BUY / SELL / HOLD)
        signal = get_final_signal(symbol)
        
        if signal == "HOLD":
            logger.info(f"Monitor: {symbol} is HOLD. No high-confidence signal.")
            continue
            
        # 2. إذا كانت هناك إشارة (BUY أو SELL)
        try:
            # (هنا يجب إضافة منطق التأكد من عدم وجود صفقة مفتوحة بالفعل)
            # ... كود التحقق من الصفقات المفتوحة ... 
            
            # نفترض الآن أنه لا توجد صفقة مفتوحة ونستمر
            
            # 3. تحديد أسعار SL و TP (نقطة الوقف والهدف)
            # هذه تحتاج إلى حساب دقيق بناءً على تحليل الشموع/الدعم، ولكن سنستخدم قيم تقديرية مؤقتاً
            
            current_price = mt5.symbol_info_tick(symbol).last
            # مثال: Stop Loss بـ 500 نقطة داخلية (50 نقطة عادية)
            SL_POINTS = 500 
            TP_POINTS = 1000 # مثال: Take Profit بـ 1000 نقطة داخلية
            
            if signal == "BUY":
                sl_price = current_price - (SL_POINTS * mt5.symbol_info(symbol).point)
                tp_price = current_price + (TP_POINTS * mt5.symbol_info(symbol).point)
            elif signal == "SELL":
                sl_price = current_price + (SL_POINTS * mt5.symbol_info(symbol).point)
                tp_price = current_price - (TP_POINTS * mt5.symbol_info(symbol).point)
            
            # 4. حساب اللوت بناءً على المخاطرة (1%)
            volume = calculate_lot_size(symbol, SL_POINTS)
            
            if volume > 0:
                # 5. تنفيذ الصفقة
                execute_trade(symbol, signal, volume, sl_price, tp_price)
                
        except Exception as e:
            logger.error(f"Error processing trade for {symbol}: {e}")
            
    logger.info("--- Trade Monitor Cycle Finished ---")


# ==================================
# جدولة المهمة الرئيسية
# ==================================

def initialize_scheduler(scheduler: AsyncIOScheduler):
    """جدولة وظيفة المراقبة لتعمل كل دقيقة."""
    
    # إضافة وظيفة المراقبة الرئيسية
    scheduler.add_job(
        trade_monitor, 
        'interval', 
        minutes=1, 
        id='trade_monitor', # هذا الـ ID يستخدمه market_timing.py للإيقاف
        replace_existing=True
    )
    
    logger.info("Trade Monitor scheduled to run every 1 minute.")
