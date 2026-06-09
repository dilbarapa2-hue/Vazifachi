# Userbot bosh fayli - Vazifa avtomatizatsiyasi
import asyncio
import json
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from config import API_ID, API_HASH, PHONE_NUMBER, SESSION_NAME, TARGET_CHANNEL
from database import add_log, update_task_status
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VazifachiUserbot:
    def __init__(self):
        self.client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        self.active_tasks = {}
    
    async def start(self):
        """Userbot ishga tushirish"""
        try:
            await self.client.start(phone=PHONE_NUMBER)
            logger.info("Userbot muvaffaqiyatli ishga tushdi")
            add_log(0, "Userbot muvaffaqiyatli ishga tushdi")
            
            # Kanal kuzatuvchisini ishga tushirish
            await self.monitor_channel()
        except SessionPasswordNeededError:
            logger.error("2FA parol kerak")
            add_log(0, "2FA parol kerak")
        except Exception as e:
            logger.error(f"Userbot xatosi: {e}")
            add_log(0, f"Userbot xatosi: {e}")
    
    async def monitor_channel(self):
        """Kanalni kuzatib turish"""
        logger.info(f"{TARGET_CHANNEL} kanalini kuzatishni boshladi")
        
        async with self.client:
            async for message in self.client.iter_messages(TARGET_CHANNEL, limit=None):
                if message.text and "ID Raqami:" in message.text:
                    task_data = self.parse_task_message(message)
                    if task_data:
                        await self.execute_task(message, task_data)
                        await asyncio.sleep(2)
    
    def parse_task_message(self, message):
        """Vazifa xabarini parsing qilish"""
        try:
            text = message.text
            lines = text.split('\n')
            
            task_data = {}
            for line in lines:
                if "ID Raqami:" in line:
                    task_data['id'] = line.split(":")[-1].strip()
                elif "Nomi:" in line:
                    task_data['name'] = line.split(":")[-1].strip()
                elif "Buyurtma soni:" in line:
                    task_data['order_count'] = line.split(":")[-1].strip()
                elif "Usernamesı:" in line:
                    task_data['username'] = line.split(":")[-1].strip()
            
            return task_data if task_data else None
        except Exception as e:
            logger.error(f"Parsing xatosi: {e}")
            return None
    
    async def execute_task(self, message, task_data):
        """Vazifani bajarish"""
        try:
            logger.info(f"Vazifa bajarilishni boshlamadi: {task_data}")
            
            # 1. 🛍 Kanal tugmasini topish va bosish
            if message.reply_markup:
                for row in message.reply_markup.rows:
                    for button in row.buttons:
                        if '🛍' in button.text or 'Kanal' in button.text:
                            await message.click(button)
                            await asyncio.sleep(3)
                            logger.info("🛍 Kanal tugmasi bosildi")
                            break
            
            # 2. Kanal/guruhga obuna bo'lish
            # Bu qadamdan keyin bot avtomatik kanal/guruhga o'tadi
            await asyncio.sleep(2)
            
            # 3. Yana xabarga qaytish
            # Ortga qaytish tugmasini topish
            if message.reply_markup:
                for row in message.reply_markup.rows:
                    for button in row.buttons:
                        if 'Ortga' in button.text or '←' in button.text:
                            await message.click(button)
                            await asyncio.sleep(1)
                            break
            
            # 4. ✅ Tasdiqlash tugmasini bosish
            await asyncio.sleep(1)
            if message.reply_markup:
                for row in message.reply_markup.rows:
                    for button in row.buttons:
                        if '✅' in button.text or 'Tasdiqlash' in button.text:
                            await message.click(button)
                            await asyncio.sleep(1)
                            logger.info("✅ Tasdiqlash tugmasi bosildi")
                            break
            
            logger.info(f"Vazifa tugallandi: {task_data['id']}")
            add_log(0, f"Vazifa tugallandi: {task_data['id']}")
            
            return True
        except Exception as e:
            logger.error(f"Vazifa xatosi: {e}")
            add_log(0, f"Vazifa bajarilishida xato: {e}")
            return False
    
    async def stop(self):
        """Userbotni o'chirish"""
        await self.client.disconnect()
        logger.info("Userbot o'chirildi")

# Userbot misoli
userbot = VazifachiUserbot()

async def run_userbot():
    """Userbotni ishga tushirish"""
    await userbot.start()

if __name__ == "__main__":
    asyncio.run(run_userbot())
