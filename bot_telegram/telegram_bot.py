from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from config import ADMIN_TELEGRAM_ID, START_MESSAGE
import logging

logger = logging.getLogger(__name__)

# ==================================
# 1. الأدوات المساعدة (لوحة المفاتيح)
# ==================================

def get_admin_keyboard():
    """إنشاء لوحة مفاتيح الأدمن التفاعلية (Inline Keyboard)."""
    keyboard = [
        [
            InlineKeyboardButton("📊 تقرير الأداء الحالي", callback_data="get_performance"),
            InlineKeyboardButton("🗒️ الصفقات المفتوحة", callback_data="open_trades"),
        ],
        [
            InlineKeyboardButton("📝 التقرير الأسبوعي الشامل", callback_data="get_weekly_report"),
        ],
        [
            InlineKeyboardButton("🛑 إيقاف/تشغيل البوت", callback_data="toggle_bot"),
            InlineKeyboardButton("🛡️ إعدادات إدارة المخاطر", callback_data="set_risk_management"),
        ],
        [
            InlineKeyboardButton("🔄 إعادة تشغيل الاتصال بـ MT5", callback_data="reconnect_mt5"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ==================================
# 2. Handlers (المستخدم العام)
# ==================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الرد على أمر /start للمستخدمين العاديين."""
    await update.message.reply_text(START_MESSAGE)
    logger.info(f"Received /start from user ID: {update.effective_user.id}")

# ==================================
# 3. Handlers (الأدمن)
# ==================================

async def admin_panel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض لوحة تحكم الأدمن."""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_TELEGRAM_ID:
        await update.message.reply_text("عفواً، لا تملك صلاحية الوصول لهذه اللوحة. هذا الأمر مخصص للأدمن فقط.")
        logger.warning(f"Unauthorized access attempt to /admin by user ID: {user_id}")
        return

    await update.message.reply_text(
        "🔐 **لوحة تحكم بوت التداول الآلي**",
        reply_markup=get_admin_keyboard(),
        parse_mode='Markdown'
    )
    logger.info(f"Admin panel displayed for user ID: {user_id}")

async def handle_admin_queries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """التعامل مع ضغطات الأزرار من لوحة الأدمن."""
    query = update.callback_query
    await query.answer() # يجب الرد على استعلام CallbackQuery لتجنب التعليق

    data = query.data
    user_id = query.from_user.id
    
    # تأكد أن المستخدم هو الأدمن
    if user_id != ADMIN_TELEGRAM_ID:
        await query.edit_message_text("عفواً، لا تملك صلاحية الوصول.")
        return
        
    response_text = f"تم اختيار: **{data}**\n\n"
    
    # ************************************************
    # هنا يتم استدعاء الدوال الحقيقية من core/jobs
    # ************************************************
    
    if data == 'toggle_bot':
        # مثال: هنا سيتم استدعاء دالة لإيقاف أو تشغيل الـ scheduler
        # Example: from jobs.scheduler_tasks import toggle_scheduler_status
        # current_status = toggle_scheduler_status(context.bot_data.get('scheduler')) 
        # response_text += f"تم تغيير حالة البوت. الحالة الحالية: {current_status}"
        response_text += "*(هذه الوظيفة ستتوقف أو تشغل الجدولة بالكامل)*"

    elif data == 'get_performance':
        response_text += "*(هذه الوظيفة ستستدعي تقرير الأداء الحالي من MT5)*"
    
    elif data == 'open_trades':
        response_text += "*(هذه الوظيفة ستستدعي قائمة الصفقات المفتوحة حالياً)*"
        
    else:
        response_text += "الوظيفة قيد التطوير..."

    # تحديث الرسالة بلوحة المفاتيح مرة أخرى
    await query.edit_message_text(response_text, reply_markup=get_admin_keyboard(), parse_mode='Markdown')

# ==================================
# 4. الإعداد النهائي للـ Handlers
# ==================================

# هذا الـ Handler سيتم إضافته لـ main.py
query_handler = CallbackQueryHandler(handle_admin_queries)
