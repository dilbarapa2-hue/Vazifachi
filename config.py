# Konfiguratsiya fayli
import os
from dotenv import load_dotenv

load_dotenv()

# Bot Tokens
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Userbot ma'lumotlari
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER", "+998")
SESSION_NAME = "userbot_session"

# Kanal ma'lumotlari
TARGET_CHANNEL = "@Obunachi_X"  # Kuzatilayotgan kanal

# Ma'lumot bazasi
DATABASE_PATH = "data/vazifachi.db"
LOGS_PATH = "data/logs.txt"

# Statuses
TASK_STATUS = {
    "PENDING": "⏳ Kutilmoqda",
    "IN_PROGRESS": "🔄 Bajarilmoqda",
    "COMPLETED": "✅ Bajarildi",
    "FAILED": "❌ Xato"
}
