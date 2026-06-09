# Vazifachi Bot - Asosiy fayli
import logging
import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from config import BOT_TOKEN
from database import init_db, add_log
from handlers import start, button_callback, receive_phone_number, error_handler
import sys

# Logging konfiguratsiyasi
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Konversatsiya states
RECEIVE_PHONE = 1

def main():
    """Bot ishga tushirish"""
    try:
        # Ma'lumot bazasini yaratish
        init_db()
        logger.info("Ma'lumot bazasi tayyorlandi")
        add_log(0, "Bot ishga tushdi")
        
        # Application yaratish
        app = Application.builder().token(BOT_TOKEN).build()
        
        # Handlers ro'yxatga olish
        # Start command
        app.add_handler(CommandHandler("start", start))
        
        # Callback query handler
        app.add_handler(CallbackQueryHandler(button_callback))
        
        # Konversatsiya handler - Akaunt qo'shish uchun
        conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(lambda u, c: RECEIVE_PHONE, pattern="^add_account$")],
            states={
                RECEIVE_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_phone_number)]
            },
            fallbacks=[CallbackQueryHandler(button_callback, pattern="^back_to_menu$")]
        )
        
        # Simpler approach - just message handler for phone input
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_phone_number))
        
        # Error handler
        app.add_error_handler(error_handler)
        
        # Botni ishga tushirish
        logger.info("🤖 Vazifachi Bot ishga tushurildi!")
        print("\n✅ Bot muvaffaqiyatli ishga tushdi!")
        print(f"📱 Bot nomini o'rganing: @Vazifachi_bot")
        print("Ctrl+C orqali to'xtating...\n")
        
        app.run_polling(allowed_updates=['message', 'callback_query'])
        
    except Exception as e:
        logger.error(f"Bot xatosi: {e}")
        add_log(0, f"Bot ishga tushmadi: {e}")
        print(f"❌ Xato: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
