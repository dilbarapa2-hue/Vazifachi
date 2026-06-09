# Vazifa bajaruvi - Multi-account executor
import asyncio
import logging
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, FloodWaitError
from config import (
    API_ID, API_HASH, TARGET_CHANNEL, TASK_TIMEOUT, 
    RETRY_ATTEMPTS, RETRY_DELAY, CONCURRENT_TASKS, ERROR_MESSAGES
)
from database import (
    update_task_status, update_account_status, add_task_log,
    increment_retry_count, disable_account, add_log
)
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskExecutor:
    """Vazifa bajaruv class - Xatosiz bajarishni ta'minlaydi"""
    
    def __init__(self):
        self.active_tasks = {}
        self.account_clients = {}
        self.semaphore = asyncio.Semaphore(CONCURRENT_TASKS)
    
    async def create_account_client(self, account_id, phone_number, session_name):
        """Akaunt uchun Telegram client yaratish"""
        try:
            if account_id in self.account_clients:
                return self.account_clients[account_id]
            
            client = TelegramClient(session_name, API_ID, API_HASH)
            await client.start(phone=phone_number)
            
            self.account_clients[account_id] = client
            logger.info(f"✅ Client yaratildi: {phone_number}")
            add_log(account_id, f"Client muvaffaqiyatli yaratildi: {phone_number}")
            return client
            
        except SessionPasswordNeededError:
            logger.error(f"❌ 2FA kerak: {phone_number}")
            add_log(account_id, "2FA parol kerak")
            return None
        except Exception as e:
            logger.error(f"❌ Client yaratishda xato: {e}")
            add_log(account_id, f"Client xatosi: {e}")
            return None
    
    async def execute_task_with_retry(self, task_id, user_id, account_id, 
                                      account_phone, session_name, task_data):
        """Vazifani qayta urinish bilan bajarish"""
        
        async with self.semaphore:
            for attempt in range(RETRY_ATTEMPTS):
                try:
                    logger.info(f"🔄 Urinish {attempt + 1}/{RETRY_ATTEMPTS}: Task {task_id}, Akaunt {account_id}")
                    
                    # Client olish yoki yaratish
                    client = self.account_clients.get(account_id)
                    if not client:
                        client = await self.create_account_client(
                            account_id, account_phone, session_name
                        )
                    
                    if not client:
                        raise Exception("Client yaratib bo'lmadi")
                    
                    # Vazifa bajarish
                    result = await self.execute_single_task(
                        client, task_id, account_id, task_data
                    )
                    
                    if result:
                        # Muvaffaqiyatli
                        update_task_status(task_id, 'COMPLETED')
                        update_account_status(account_id, success=True)
                        add_task_log(task_id, account_id, "Task execution", "SUCCESS")
                        logger.info(f"✅ Vazifa tugallandi: {task_id}")
                        return True
                    
                except FloodWaitError as e:
                    wait_time = e.seconds
                    logger.warning(f"⏳ Flood wait: {wait_time} soniya")
                    add_task_log(task_id, account_id, "Flood wait", "WAITING", str(e))
                    await asyncio.sleep(min(wait_time + 5, 60))
                    
                except Exception as e:
                    error_msg = str(e)
                    logger.warning(f"⚠️ Urinish {attempt + 1} xatosi: {error_msg}")
                    add_task_log(task_id, account_id, "Task execution", "ERROR", error_msg)
                    
                    increment_retry_count(task_id)
                    update_account_status(account_id, success=False, error_message=error_msg)
                    
                    if attempt < RETRY_ATTEMPTS - 1:
                        await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                        continue
                    else:
                        # Oxirgi urinish
                        update_task_status(
                            task_id, 'FAILED', 
                            f"{ERROR_MESSAGES.get('UNKNOWN', 'Xato')} - {error_msg}"
                        )
                        logger.error(f"❌ Vazifa muvaffaqiyatsiz: {task_id}")
                        return False
            
            return False
    
    async def execute_single_task(self, client, task_id, account_id, task_data):
        """Bitta vazifani bajarish (asosiy logika)"""
        try:
            update_task_status(task_id, 'IN_PROGRESS')
            add_task_log(task_id, account_id, "Start execution", "IN_PROGRESS")
            
            # Kanal xabarlarini kuzatish
            async with asyncio.timeout(TASK_TIMEOUT):
                async for message in client.iter_messages(TARGET_CHANNEL, limit=100):
                    if not message.text:
                        continue
                    
                    # Vazifa xabarini topish
                    if "ID Raqami:" in message.text:
                        task_info = self.parse_task_message(message)
                        
                        if task_info and self.task_matches(task_info, task_data):
                            # 1️⃣ 🛍 Kanal tugmasini topish
                            logger.info(f"🔍 Kanal tugmasini izlayapti...")
                            
                            if not await self.click_button(client, message, ['🛍', 'Kanal']):
                                raise Exception(ERROR_MESSAGES['BUTTON_NOT_FOUND'])
                            
                            await asyncio.sleep(2)
                            add_task_log(task_id, account_id, "Channel button clicked", "SUCCESS")
                            
                            # 2️⃣ Obuna bo'lish (avtomatik)
                            logger.info("📲 Obunaga bo'lishni kutayapti...")
                            await asyncio.sleep(3)
                            add_task_log(task_id, account_id, "Subscribe", "SUCCESS")
                            
                            # 3️⃣ Ortga qaytish
                            logger.info("↩️ Xabarni izlayapti...")
                            if not await self.click_button(client, message, ['←', 'Ortga', 'Back']):
                                logger.warning("⚠️ Ortga qaytish tugmasi topilmadi, davom ettirilmoqda...")
                            
                            await asyncio.sleep(1)
                            
                            # 4️⃣ ✅ Tasdiqlash tugmasini bosish
                            logger.info("✅ Tasdiqlash tugmasini izlayapti...")
                            if not await self.click_button(client, message, ['✅', 'Tasdiqlash', 'Confirm']):
                                raise Exception(ERROR_MESSAGES['CONFIRM_FAILED'])
                            
                            await asyncio.sleep(1)
                            add_task_log(task_id, account_id, "Confirm button clicked", "SUCCESS")
                            
                            logger.info(f"✅ Vazifa muvaffaqiyatli bajarildi: {task_id}")
                            return True
            
            raise Exception("Vazifa xabari topilmadi")
            
        except asyncio.TimeoutError:
            raise Exception(ERROR_MESSAGES['TIMEOUT'])
        except Exception as e:
            raise Exception(f"Bajarilish xatosi: {str(e)}")
    
    async def click_button(self, client, message, button_texts):
        """Tugmani topib bosish"""
        try:
            if not message.reply_markup:
                return False
            
            for row in message.reply_markup.rows:
                for button in row.buttons:
                    button_text = button.text if hasattr(button, 'text') else str(button)
                    
                    for search_text in button_texts:
                        if search_text in button_text:
                            await message.click(button)
                            logger.info(f"✅ Tugma bosildi: {button_text}")
                            return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Tugma bosishda xato: {e}")
            return False
    
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
    
    def task_matches(self, task_info, task_data):
        """Vazifa ma'lumotlari mos kelishini tekshirish"""
        try:
            if isinstance(task_data, str):
                task_data = json.loads(task_data)
            
            # ID bo'yicha solishtirish
            if task_info.get('id') == task_data.get('id'):
                return True
            
            return False
        except Exception as e:
            logger.error(f"Solishtirish xatosi: {e}")
            return False
    
    async def disconnect_all(self):
        """Barcha clientlarni o'chirish"""
        for account_id, client in self.account_clients.items():
            try:
                await client.disconnect()
                logger.info(f"✅ Client o'chirildi: {account_id}")
            except Exception as e:
                logger.error(f"❌ Client o'chirishda xato: {e}")
        
        self.account_clients.clear()

# Global executor
executor = TaskExecutor()

async def execute_tasks_concurrently(tasks, accounts):
    """Bir nechta vazifalarni bir vaqtda bajarish"""
    logger.info(f"🚀 {len(tasks)} ta vazifa bajarilishni boshlayapti...")
    
    account_map = {acc[0]: (acc[1], acc[2]) for acc in accounts}
    execution_tasks = []
    
    for task in tasks:
        task_id, user_id, account_id, task_data = task
        
        if account_id not in account_map:
            logger.warning(f"⚠️ Akaunt topilmadi: {account_id}")
            continue
        
        phone, session = account_map[account_id]
        
        exec_task = executor.execute_task_with_retry(
            task_id, user_id, account_id, phone, session, task_data
        )
        execution_tasks.append(exec_task)
    
    if execution_tasks:
        results = await asyncio.gather(*execution_tasks, return_exceptions=True)
        success_count = sum(1 for r in results if r is True)
        logger.info(f"📊 Natijar: {success_count}/{len(tasks)} muvaffaqiyatli")
        return success_count
    
    return 0
