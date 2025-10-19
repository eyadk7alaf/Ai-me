# Python code goes here
import MetaTrader5 as mt5
import pandas as pd
import logging
from config import TRADING_SYMBOLS, TIMEFRAMES
from core.mt5_trading import initialize_mt5 # لاستدعاء تهيئة MT5

logger = logging.getLogger(__name__)

# ==================================
# 1. جلب البيانات من MT5
# ==================================

def get_symbol_data(symbol: str, timeframe_str: str, bars: int = 300):
    """
    جلب بيانات الشموع من MT5 لإطار زمني معين.
    """
    
    # تحويل الإطار الزمني من الاسم النصي إلى ثابت MT5
    if timeframe_str == 'H4':
        mt5_tf = mt5.TIMEFRAME_H4
    elif timeframe_str == 'H1':
        mt5_tf = mt5.TIMEFRAME_H1
    elif timeframe_str == 'M15':
        mt5_tf = mt5.TIMEFRAME_M15
    else:
        logger.error(f"Invalid timeframe: {timeframe_str}")
        return None

    # جلب البيانات
    rates = mt5.copy_rates_from_pos(symbol, mt5_tf, 0, bars)
    if rates is None or len(rates) == 0:
        logger.warning(f"Failed to get data for {symbol} on {timeframe_str}. Error: {mt5.last_error()}")
        return None
        
    # تحويل البيانات إلى DataFrame لتسهيل التحليل
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

# ==================================
# 2. أنظمة التحليل الخمسة (Logic Placeholders)
# يجب أن ترجع "BUY" أو "SELL" أو "HOLD"
# ==================================

def check_system_1_trend(data_df: pd.DataFrame):
    """النظام 1: تحليل الاتجاه العام (مثل المتوسطات المتحركة الطويلة)."""
    # **ضع كود استراتيجية الاتجاه هنا**
    return "HOLD"

def check_system_2_momentum(data_df: pd.DataFrame):
    """النظام 2: تحليل الزخم والقوة (مثل RSI أو Stochastic)."""
    # **ضع كود استراتيجية الزخم هنا**
    return "HOLD"

def check_system_3_snr(data_df: pd.DataFrame):
    """النظام 3: تحليل الدعم والمقاومة أو مناطق العرض والطلب."""
    # **ضع كود تحليل المناطق هنا**
    return "HOLD"
        
def check_system_4_candle_conf(data_df: pd.DataFrame):
    """النظام 4: تأكيد نماذج الشموع (على إطار الدخول M15)."""
    # **ضع كود تحليل الشموع هنا**
    return "HOLD"

def check_system_5_volume_conf(data_df: pd.DataFrame):
    """النظام 5: تحليل حجم التداول (Volume) لتأكيد قوة الحركة."""
    # **ضع كود تحليل الحجم هنا**
    return "HOLD"

# ==================================
# 3. اتخاذ القرار النهائي (دمج الأطر الزمنية والـ 5 أنظمة)
# ==================================

def get_final_signal(symbol: str):
    """
    تحليل شامل يدمج قرارات الأنظمة الخمسة عبر الأطر الزمنية الثلاثة.
    """
    # تهيئة الاتصال بـ MT5
    if not initialize_mt5():
        return "HOLD"
    
    # قائمة بقرارات الشراء/البيع المتفق عليها عبر كل الأطر الزمنية
    all_timeframe_signals = [] 

    # المرور على الأطر الزمنية بالتسلسل (من H4 إلى M15)
    for tf_name, tf_value in TIMEFRAMES.items():
        data = get_symbol_data(symbol, tf_value)
        if data is None:
            return "HOLD"

        # 1. إجراء فحص الأنظمة الخمسة على البيانات الحالية
        results = [
            check_system_1_trend(data),
            check_system_2_momentum(data),
            check_system_3_snr(data),
            check_system_4_candle_conf(data),
            check_system_5_volume_conf(data) 
        ]
        
        # 2. شرط الاتفاق: يجب أن تتفق كل الأنظمة الخمسة على نفس الإشارة
        unique_signals = set(results)
        
        if len(unique_signals) == 1 and "HOLD" not in unique_signals:
            # تم الاتفاق في هذا الإطار الزمني
            current_signal = results[0]
            all_timeframe_signals.append(current_signal)
        else:
            # إذا فشل الاتفاق في أي إطار زمني، يتم إلغاء الصفقة بالكامل
            logger.info(f"Analysis failed to reach 5/5 consensus on {symbol} / {tf_value}.")
            return "HOLD"
    
    # 3. الشرط النهائي: يجب أن يتفق قرار جميع الأطر الزمنية على نفس الإشارة
    if len(set(all_timeframe_signals)) == 1 and all_timeframe_signals[0] != "HOLD":
        logger.info(f"FINAL HIGH-CONFIDENCE DECISION FOR {symbol}: {all_timeframe_signals[0]}")
        return all_timeframe_signals[0] # BUY أو SELL
    
    # في حال وجود تعارض أو عدم وجود إشارة
    return "HOLD"
