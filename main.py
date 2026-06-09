# Vazifachi Bot - Asosiy fayli (Multi-account version)
import logging
import asyncio
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ConversationHandler
)
from config import BOT_TOKEN
from database import init_db, add_log, get_pending_tasks, get_active_accounts
from handlers import start, button_callback, receive_phone_number, error_handler, RECEIVE_PHONE
from task_executor import execute_tasks_concurrently, executor
import sys

# Logging konfiguratsiyasi
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class VazifachiBot:
    def __init__(self):
        self.app = None
        self.task_runner_enabled = False
    
    def setup_handlers(self):
        """Barcha handler larni ro'yxatga olish"""
        
        # Start command
        self.app.add_handler(CommandHandler("start", start))
        
        # Callback query handler
        self.app.add_handler(CallbackQueryHandler(button_callback))
        
        # Konversatsiya handler - Akaunt qo'shish uchun
        conv_handler = ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    lambda u, c: RECEIVE_PHONE, 
                    pattern="^add_account$"
                )
            ],
            states={
                RECEIVE_PHONE: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND, 
                        receive_phone_number
                    )
                ]
            },
            fallbacks=[
                CallbackQueryHandler(button_callback, pattern="^back_to_menu$")
            ]
        )
        
        self.app.add_handler(conv_handler)
        
        # Message handler
        self.app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, 
                receive_phone_number
            )
        )
        
        # Error handler
        self.app.add_error_handler(error_handler)
    
    async def task_executor_loop(self):
        """Vazifalarni avtomatik bajaradigan loop"""
        logger.info("🔄 Vazifa bajaruvi loop ishga tushdi")
        
        while self.task_runner_enabled:
            try:
                # Kutilmoqda bo'lgan vazifalarni olish
                pending_tasks = get_pending_tasks(limit=5)
                
                if pending_tasks:
                    logger.info(f"📋 {len(pending_tasks)} ta vazifa topildi")
                    
                    # Har bir vazifa uchun akount topish
                    task_with_accounts = []
                    for task in pending_tasks:
                        task_id, user_id, account_id, task_data = task
                        accounts = get_active_accounts(user_id)
                        
                        if accounts:
                            task_with_accounts.append((task_id, user_id, account_id, task_data))
                    
                    if task_with_accounts:
                        accounts = get_active_accounts(task_with_accounts[0][1])
                        
                        # Vazifalarni bajarish
                        success_count = await execute_tasks_concurrently(
                            task_with_accounts,
                            accounts
                        )
                        
                        logger.info(f"✅ {success_count} ta vazifa tugallandi")
                
                # 10 soniya kutish
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.error(f"❌ Vazifa bajaruv loop xatosi: {e}")
                await asyncio.sleep(5)
    
    async def start_task_runner(self):
        """Vazifa bajaruv loop ni ishga tushirish"""
        self.task_runner_enabled = True
        await self.task_executor_loop()
    
    async def stop_task_runner(self):
        """Vazifa bajaruv loop ni to'xtatish"""
        self.task_runner_enabled = False
        await executor.disconnect_all()
    
    async def post_init(self, app):
        """Bot ishga tushgandan keyin"""
        logger.info("✅ Bot tayyorlandi")
        
        # Vazifa bajaruv loop ni background da ishga tushirish
        asyncio.create_task(self.start_task_runner())
    
    async def post_stop(self, app):
        """Bot o'chirilgandan oldin"""
        logger.info("❌ Bot o'chirilmoqda")
        await self.stop_task_runner()
    
    def main(self):
        """Bot ishga tushirish"""
        try:
            # Ma'lumot bazasini yaratish
            init_db()
            logger.info("✅ Ma'lumot bazasi tayyorlandi")
            add_log(0, "Bot ishga tushdi")
            
            # Application yaratish
            self.app = Application.builder().token(BOT_TOKEN).build()
            
            # Lifecycle handlers
            self.app.post_init = self.post_init
            self.app.post_stop = self.post_stop
            
            # Handlers ro'yxatga olish
            self.setup_handlers()
            
            # Botni ishga tushirish
            logger.info("\n" + "="*50)
            logger.info("🤖 Vazifachi Bot ishga tushurildi!")
            logger.info("="*50)
            print("\n✅ Bot muvaffaqiyatli ishga tushdi!")
            print("📱 Bot nomini o'rganing: @Vazifachi_bot")
            print("🔄 Vazifa bajaruvi loop ishga tushdi")
            print("💾 Ma'lumot bazasi: data/vazifachi.db")
            print("📝 Loglar: data/logs.txt")
            print("Ctrl+C orqali to'xtating...\n")
            
            self.app.run_polling(
                allowed_updates=['message', 'callback_query'],
                drop_pending_updates=True
            )
            
        except KeyboardInterrupt:
            logger.info("🛑 Bot foydalanuvchi tomonidan to'xtatildi")
            add_log(0, "Bot to'xtatildi")
        except Exception as e:
            logger.error(f"❌ Bot xatosi: {e}")
            add_log(0, f"Bot ishga tushmadi: {e}")
            print(f"❌ Xato: {e}")
            sys.exit(1)

def main():
    """Asosiy entry point"""
    bot = VazifachiBot()
    bot.main()

if __name__ == "__main__":
    main()
