# 🤖 Vazifachi - Telegram Bot

**Vazifachi** - @Obunachi_X kanalining vazifalarini avtomatik bajaradigan intelli Telegram boti.

## ✨ Asosiy Xususiyatlari

✅ **Akaunt Boshqaruvi** - Bir nechta Telegram akountni qo'shish va boshqarish
🔄 **Avtomatik Vazifa Bajarish** - @Obunachi_X kanalidan vazifalarni avtomatik olish va bajarish
📊 **Statistika** - Jami vazifalar, tugallangan va muvaffaqiyatsiz vazifalar
📝 **Loglar** - Barcha amallarning to'liq tarixini saqlash
🛡️ **Xavfsizlik** - User session management bilan xavfsizilik

## 📋 Asosiy Menyu

Bot `/start` buyrug'i orqali ishga tushtirilganda quyidagi menyuni ko'rsatadi:

1. **➕ Akaunt qo'shish** - Yangi Telegram akountni ulash
2. **📱 Akautlar** - Qo'shilgan akountlar ro'yxati
3. **📊 Statistika** - Vazifa statistikasi
4. **📝 Loglar** - Jarayonlar tarixli logi

## 🎯 Vazifa Bajarish Jarayoni

Bot quyidagi bosqichlarni avtomatik bajaradi:

1. 🔍 @Obunachi_X kanalini kuzatib turadi
2. 📬 Yangi vazifa xabarini sezadi
3. 🛍️ **Kanal** tugmasini topib bosadi
4. 🔗 Kanal/Guruhga o'tib obuna bo'ladi
5. ↩️ Asosiy xabarga qaytadi
6. ✅ **Tasdiqlash** tugmasini bosadi
7. 🔄 Yangi vazifani kutib qoladi

## 🚀 O'rnatish va Ishga Tushirish

### 1️⃣ Loyihani Clone Qilish

```bash
git clone https://github.com/dilbarapa2-hue/Vazifachi.git
cd Vazifachi
```

### 2️⃣ Virtual Muhitni Yaratish

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 3️⃣ Kutubxonalarni O'rnatish

```bash
pip install -r requirements.txt
```

### 4️⃣ Konfiguratsiyani Tayyorlash

`.env.example` faylini `.env` deb nomini o'zgartiring va ma'lumotlarni kiriting:

```bash
cp .env.example .env
```

**`.env` faylini to'ldirish:**

#### Bot Token
1. **@BotFather** bota yozing
2. `/newbot` buyrug'idan keyin bot nomi va usernameni kiriting
3. Token ni `.env` ga qo'ying

```env
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

#### API ID va API Hash
1. https://my.telegram.org ga kiring
2. "API development tools" bo'limiga kiring
3. `api_id` va `api_hash` ni oling
4. `.env` ga qo'ying

```env
API_ID=123456
API_HASH=0123456789abcdef0123456789abcdef
```

#### Telefon Raqami va Admin ID
```env
PHONE_NUMBER=+998901234567
ADMIN_ID=123456789
```

### 5️⃣ Botni Ishga Tushirish

```bash
python main.py
```

## 📁 Loyiha Tuzilishi

```
Vazifachi/
├── config.py              # Konfiguratsiya
├── database.py            # Ma'lumot bazasi
├── userbot.py             # Userbot (Vazifa avtomatizatsiyasi)
├── handlers.py            # Message handlers
├── main.py                # Bot asosiy fayli
├── requirements.txt       # Kutubxonalar
├── .env.example           # .env shabloni
├── data/
│   ├── vazifachi.db       # SQLite ma'lumot bazasi
│   └── logs.txt           # Loglar fayli
└── README.md              # Bu fayl

```

## 🔧 Konfiguratsiya

`config.py` faylida o'zgartirishlar:

```python
# Kuzatilayotgan kanal
TARGET_CHANNEL = "@Obunachi_X"

# Ma'lumot bazasi yo'li
DATABASE_PATH = "data/vazifachi.db"
LOGS_PATH = "data/logs.txt"
```

## 📊 Ma'lumot Bazasi Struktura

### `accounts` - Akountlar jadvali
- `id` - Akaunt ID
- `user_id` - Telegram foydalanuvchi ID
- `phone_number` - Telefon raqami
- `session_name` - Sesiya nomi
- `is_active` - Faollik statusi
- `created_at` - Yaratilgan vaqt

### `tasks` - Vazifalar jadvali
- `id` - Vazifa ID
- `user_id` - Foydalanuvchi ID
- `account_id` - Akaunt ID
- `task_data` - Vazifa ma'lumotlari (JSON)
- `status` - Status (PENDING, IN_PROGRESS, COMPLETED, FAILED)
- `created_at` - Yaratilgan vaqt
- `completed_at` - Tugallangan vaqt

### `statistics` - Statistika jadvali
- `user_id` - Foydalanuvchi ID
- `total_tasks` - Jami vazifalar
- `completed_tasks` - Tugallangan vazifalar
- `failed_tasks` - Muvaffaqiyatsiz vazifalar

## 🎮 Bot Buyruqlari

| Buyruq | Tavsifi |
|--------|---------|
| `/start` | Botni ishga tushirish |
| `/menu` | Asosiy menyu |
| `/stats` | Statistika |
| `/logs` | Loglar |

## ⚙️ Texnik Detallar

- **Python 3.8+** talab qilinadi
- **SQLite 3** ma'lumot bazasi
- **Telethon** - Userbot uchun
- **python-telegram-bot** - Bot uchun

## 🐛 Xatolarni Tuzatish

### Bot bosmayapti?
```bash
# .env faylini tekshiring
cat .env

# Loglarni ko'ring
tail -f data/logs.txt
```

### Userbot ulanmayapti?
```bash
# 2FA parol kerak bo'lishi mumkin
# Konsolda parol kiritish uchun kutib qoladi
```

## 📞 Yordam va Aloqa

Agar savol yoki taklif bo'lsa:
- 🐛 GitHub Issues ga yozing
- 📧 Admin bilan bog'lanish uchun BotFather ga yozing

## 📜 Litsenziya

Bu loyiha **MIT License** ostida tarqatiladi.

---

**Vazifachi - Sizning Vazifalar, Bot Bajaradi!** 🚀

Qo'shimcha ma'lumot uchun README ni ko'rib chiqing yoki `config.py` ga nazar tashlab ko'ring.

**Muvaffaqiyati tilasiz!** ✨
