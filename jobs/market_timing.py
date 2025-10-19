from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

logger = logging.getLogger(__name__)

# ==================================
# إعدادات أوقات الإيقاف والتشغيل التلقائي (بالتوقيت المحلي للخادم)
# ==================================
STOP_DAY = 4    # 4 = يوم الجمعة (Mon=0, Tue=1, ..., Sun=6)
STOP_HOUR = 23  # الساعة 23:00 (11 مساءً)
START_DAY = 6   # 6 = يوم الأحد
START_HOUR = 23 # الساعة 23:00 (11 مساءً - بداية الافتتاح الآسيوي)

# ==================================
# وظائف الإيقاف/التشغيل التلقائي
# ==================================

def toggle_trade_monitor(scheduler: AsyncIOScheduler, enable: bool):
    """تفعيل أو تعطيل وظيفة المراقبة والتحليل الرئيسية."""
    try:
        if enable:
            # resume_job تستأنف الوظيفة التي تم تعريفها بالـ id 'trade_monitor'
            scheduler.resume_job('trade_monitor') 
            logger.info("Market resumed: Trade monitoring is now ON.")
        else:
            scheduler.pause_job('trade_monitor')
            logger.info("Market paused: Trade monitoring is OFF (Weekend Stop).")
    except Exception as e:
        # هذه المشكلة تحدث إذا لم تكن الوظيفة trade_monitor موجودة أو مفعلة
        logger.error(f"Failed to toggle trade_monitor job: {e}")

def schedule_weekend_stop(scheduler: AsyncIOScheduler):
    """جدولة وظيفة إيقاف التداول ليوم الجمعة."""
    scheduler.add_job(
        func=lambda: toggle_trade_monitor(scheduler, False),
        trigger='cron',
        day_of_week=STOP_DAY,
        hour=STOP_HOUR,
        id='weekend_stop',
        replace_existing=True
    )

def schedule_weekend_start(scheduler: AsyncIOScheduler):
    """جدولة وظيفة بدء التداول ليوم الأحد (الافتتاح)."""
    scheduler.add_job(
        func=lambda: toggle_trade_monitor(scheduler, True),
        trigger='cron',
        day_of_week=START_DAY,
        hour=START_HOUR,
        id='weekend_start',
        replace_existing=True
    )

def initialize_market_timer(scheduler: AsyncIOScheduler):
    """تشغيل وظائف الجدولة للإيقاف والتشغيل الأسبوعي."""
    schedule_weekend_stop(scheduler)
    schedule_weekend_start(scheduler)
    logger.info("Market timing jobs scheduled successfully.")
