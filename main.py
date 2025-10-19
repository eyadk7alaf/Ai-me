import logging
import MetaTrader5 as mt5 # نحتاجه للـ shutdown في حال فشل التهيئة
from telegram.ext import ApplicationBuilder, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# استيراد الثوابت الأساسية
from config import TELEGRAM_BOT_TOKEN
# استيراد Handlers التليجرام
from bot_telegram.telegram_bot import start_command, admin_panel_command, query_handler
# استيراد وظائف الجدولة والمهام
from jobs.market_timing import initialize_market_timer
from jobs.scheduler_tasks import initialize_scheduler
from core.mt5_trading import initialize_mt5 # لوظيفة التهيئة الأولية

# ==================================
# إعدادات التسجيل (Logging)
# ==================================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_bot():
    """تشغيل البوت، تهيئة MT5، وبدء الجدولة."""
    
    # 1. محاولة تهيئة MT5 أولاً (ضروري قبل بدء أي شيء)
    if not initialize_mt5():
        logger.error("FATAL ERROR: Failed to initialize and login to MT5. Exiting.")
        # نستخدم mt5.shutdown() لضمان الإغلاق النظيف إذا فشل الاتصال
        mt5.shutdown() 
        return

    # 2. تهيئة الجدولة (Scheduler)
    scheduler = AsyncIOScheduler()
    initialize_scheduler(scheduler)       # جدولة وظيفة trade_monitor كل دقيقة
    initialize_market_timer(scheduler)    # جدولة الإيقاف/التشغيل الأسبوعي

    # 3. تهيئة التليجرام
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Handlers 
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('admin', admin_panel_command))
    application.add_handler(query_handler) # للتعامل مع أزرار Inline Keyboard

    # 4. بدء التشغيل
    try:
        scheduler.start()
        logger.info("Scheduler started successfully. Starting Telegram Bot polling...")
        application.run_polling()
    except Exception as e:
        logger.critical(f"A critical error occurred during bot execution: {e}")
    finally:
        # إغلاق MT5 بشكل نظيف عند إيقاف البرنامج
        mt5.shutdown() 
        logger.info("Bot stopped. MT5 connection shut down.")


if __name__ == '__main__':
    run_bot()
