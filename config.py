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

# Kanal ma'lumotlari
TARGET_CHANNEL = "@Obunachi_X"

# Ma'lumot bazasi
DATABASE_PATH = "data/vazifachi.db"
LOGS_PATH = "data/logs.txt"

# Akauntlar boshqaruvi
MAX_ACCOUNTS = 10  # Maksimal 10 ta akaunt
CONCURRENT_TASKS = 5  # Bir vaqtda 5 ta vazifa bajariladi
TASK_TIMEOUT = 120  # Vazifa timeout (sekund)
RETRY_ATTEMPTS = 3  # Xato bo'lsa qayta urinish
RETRY_DELAY = 5  # Qayta urinish vaqti (sekund)

# Statuses
TASK_STATUS = {
    "PENDING": "⏳ Kutilmoqda",
    "IN_PROGRESS": "🔄 Bajarilmoqda",
    "COMPLETED": "✅ Bajarildi",
    "FAILED": "❌ Xato",
    "RETRY": "🔁 Qayta urinish"
}

# Xato xabarlar
ERROR_MESSAGES = {
    "BUTTON_NOT_FOUND": "🛍 yoki Kanal tugmasi topilmadi",
    "SUBSCRIBE_FAILED": "Obunaga bo'lish muvaffaqiyatsiz bo'ldi",
    "CONFIRM_FAILED": "✅ Tasdiqlash tugmasi topilmadi",
    "TIMEOUT": "Vazifa vaqti tugadi",
    "SESSION_ERROR": "Sessiya xatosi",
    "UNKNOWN": "Noma'lum xato"
}

# Logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"
