import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

from .config import settings
# این بخش‌ها بعداً با منطق اصلی شما پر می‌شوند
# from . import crud, schemas
# from .database import SessionLocal

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# این یک دیکشنری ساده برای نگهداری وضعیت گفتگوی کاربران در MVP است
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    user = update.effective_user
    chat_id = user.id
    
    # TODO: Check user role from DB
    # db = SessionLocal()
    # db_user = crud.get_user_by_chat_id(db, chat_id=chat_id)
    # db.close()
    
    # فرض می‌کنیم برای تست، یک کاربر دکتر با آیدی مشخص داریم
    # در نسخه واقعی، این بخش باید با دیتابیس چک شود
    if chat_id == 123456789: # TODO: Replace with your doctor's chat_id for testing
        role = "DOCTOR"
    else:
        role = "PATIENT"

    if role == "DOCTOR":
        keyboard = [
            [InlineKeyboardButton("➕ افزودن بیمار", callback_data='add_patient')],
            [InlineKeyboardButton("👥 لیست بیماران من", callback_data='list_patients')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("سلام دکتر. به پنل مدیریت خوش آمدید.", reply_markup=reply_markup)
    else:
        await update.message.reply_text(f"سلام {user.first_name}. به سیستم پیگیری هوشمند خوش آمدید.")

async def handle_button_press(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'add_patient':
        user_states[query.from_user.id] = 'AWAITING_PATIENT_NAME'
        await query.edit_message_text(text="لطفا نام کامل بیمار را ارسال کنید:")

    # TODO: Handle other button presses

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular text messages."""
    chat_id = update.effective_chat.id
    text = update.message.text

    # چک کردن وضعیت فعلی کاربر
    state = user_states.get(chat_id)

    if state == 'AWAITING_PATIENT_NAME':
        # TODO: Save patient name and ask for the next info (e.g., chat_id)
        logger.info(f"Patient name received: {text}")
        await update.message.reply_text("متشکرم. حالا شناسه تلگرام بیمار را وارد کنید.")
        user_states[chat_id] = 'AWAITING_PATIENT_CHAT_ID'
    else:
        # این حالت برای پاسخ‌های بیمار به سوالات فالوآپ است
        # TODO: Send the response to the AI service for processing
        logger.info(f"Received response from patient {chat_id}: {text}")
        await update.message.reply_text("پاسخ شما ثبت شد. متشکرم.")


def setup_bot_handlers(application: Application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_button_press))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return application