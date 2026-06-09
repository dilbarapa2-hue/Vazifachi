# 🤖 Vazifachi - Telegram Bot Vazifa Bajaruvi

**Vazifachi** - @Obunachi_X kanalining vazifalarini avtomatik bajaradigan intelli Telegram boti.

> **10 ta akountni bir vaqtda boshqaradi | 5 ta vazifani parallel bajaradi | Avtomatik xato tuzatish**

## ✨ Asosiy Xususiyatlari

### 🎯 Multi-Account Support
- ✅ Bir vaqtda **10 tagacha Telegram akount**ni boshqarish
- 🔄 **5 ta vazifa**ni bir vaqtda parallel bajarilishi
- 📊 Har bir akount uchun **alohida statistika**
- ⚡ Eng ko'p xatoga uchraydigan akountni avtomatik o'chirish

### 🛡️ Xato Tuzatish va Ishonchilik
- 🔁 **3 marta qayta urinish** xato bo'lsa
- ⏳ Flood wait (rate limit) ni avtomatik boshqarish
- 📝 **To'liq task log** - har bir jarayonni kuzatish
- 🚨 Sessiya xatolarini avtomatik aniqlash

### 📊 Kuzatish va Statistika
- 📈 Real-time statistika (jami, tugallangan, muvaffaqiyatsiz vazifalar)
- 📱 Akount bo'yicha alohida natijalar
- 📝 Barcha amallarning to'liq logi
- 🔍 Xato kuzatish va debugging

### 🚀 Avtomatsiya
- ⏰ Har 10 soniyada vazifalarni tekshirish
- 🔄 Kutilmoqda bo'lgan vazifalarni avtomatik bajarilishi
- 🎯 Tugma va kanal topib avtomatik bosish
- ✅ Tugallangan vazifalarni avtomatik belgilash

## 📋 Asosiy Menyu

Bot `/start` buyrug'i orqali ishga tushtirilganda quyidagi menyuni ko'rsatadi:

```
🏠 ASOSIY MENYU
├── ➕ Akaunt qo'shish      → Yangi Telegram akountni ulash
├── 📱 Akautlar            → Qo'shilgan akountlar ro'yxati
├── 📊 Statistika          → Vazifa statistikasi
└── 📝 Loglar              → Jarayonlar tarixli logi
```

## 🎯 Vazifa Bajarish Jarayoni

Bot quyidagi bosqichlarni avtomatik bajaradi:

```
1️⃣  🔍 @Obunachi_X kanalini kuzatib turadi
    ↓
2️⃣  📬 Yangi vazifa xabarini sezadi
    ↓
3️⃣  🛍️  "🛍 Kanal" tugmasini topib bosadi
    ↓
4️⃣  🔗 Kanal/Guruhga o'tib avtomatik obuna bo'ladi
    ↓
5️⃣  ↩️  Asosiy xabarga qaytadi
    ↓
6️⃣  ✅ "✅ Tasdiqlash" tugmasini bosadi
    ↓
7️⃣  🎉 Vazifa tugallandi!
```

### Xato bo'lsa:
```
❌ Xato aniqlandi
  ↓
🔁 Qayta urinish (1-3 marta)
  ↓
📝 Xatoni logga yozish
  ↓
❌ 3 ta xato bo'lsa → Akountni deaktiv qilish
```

## 🚀 O'rnatish va Ishga Tushirish

### 1️⃣ Loyihani Clone Qilish

```bash
git clone https://github.com/dilbarapa2-hue/Vazifachi.git
cd Vazifachi
```

### 2️⃣ Virtual Muhit Yaratish

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Kutubxonalarni O'rnatish

```bash
pip install -r requirements.txt
```

### 4️⃣ Konfiguratsiyani Tayyorlash

```bash
cp .env.example .env
```

**Keyin `.env` faylini matn editorida oching va to'ldiring:**

```env
# Bot Token (BotFather orqali)
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Telegram API ma'lumotlari (my.telegram.org dan)
API_ID=123456
API_HASH=0123456789abcdef0123456789abcdef

# Admin Telegram ID
ADMIN_ID=123456789
```

### 🔑 Ma'lumotlarni Qanday Olish?

#### **BOT_TOKEN** (BotFather orqali):
1. Telegram da **@BotFather** ni topish
2. `/newbot` buyrug'ini yozing
3. Bot nomini va usernameni kiriting (masalan: Vazifachi, @Vazifachi_bot)
4. **Token** ni olib `.env` ga qo'ying

```
✅ Bot yaratildi!
Token: 123456:ABC-DEF...
```

#### **API_ID va API_HASH** (my.telegram.org dan):
1. https://my.telegram.org ga kiring
2. Telegram akountga kiring (OTP kod kiriting)
3. "API development tools" bo'limiga o'tish
4. App yaratish (App title, Short name)
5. **api_id** va **api_hash** ni olib `.env` ga qo'ying

#### **ADMIN_ID**:
- Sizning Telegram ID raqamingiz
- @userinfobot botiga `/start` yozing
- Chiqadigan sonlarni olib saqlang (masalan: 123456789)

### 5️⃣ Botni Ishga Tushirish

```bash
python main.py
```

**Agar muvaffaqiyatli bo'lsa:**
```
==================================================
🤖 Vazifachi Bot ishga tushurildi!
==================================================

✅ Bot muvaffaqiyatli ishga tushdi!
📱 Bot nomini o'rganing: @Vazifachi_bot
🔄 Vazifa bajaruvi loop ishga tushdi
💾 Ma'lumot bazasi: data/vazifachi.db
📝 Loglar: data/logs.txt
Ctrl+C orqali to'xtating...
```

## 📁 Loyiha Tuzilishi

```
Vazifachi/
├── config.py              # Asosiy konfiguratsiya
├── database.py            # Ma'lumot bazasi boshqaruvi
├── task_executor.py       # Vazifa bajaruv engine
├── handlers.py            # Bot message handlers
├── main.py                # Bot asosiy fayli
├── requirements.txt       # Python kutubxonalari
├── .env.example           # Konfiguratsiya shabloni
├── .gitignore             # Git ignore
├── README.md              # Bu fayl
└── data/                  # Ma'lumot papkasi
    ├── vazifachi.db       # SQLite ma'lumot bazasi
    └── logs.txt           # Barcha loglar
```

## ⚙️ Konfiguratsiya

### `config.py` - Asosiy sozlamalar

```python
MAX_ACCOUNTS = 10          # Maksimal 10 ta akaunt
CONCURRENT_TASKS = 5       # Bir vaqtda 5 ta vazifa
TASK_TIMEOUT = 120         # Vazifa timeout (sekund)
RETRY_ATTEMPTS = 3         # Qayta urinish soni
RETRY_DELAY = 5            # Qayta urinish vaqti (sekund)
TARGET_CHANNEL = "@Obunachi_X"  # Kuzatilayotgan kanal
```

## 📊 Ma'lumot Bazasi Struktura

### `accounts` jadvali
```sql
id              - Akaunt ID
user_id         - Telegram foydalanuvchi ID
phone_number    - Telefon raqami (UNIQUE)
session_name    - Sesiya nomi
is_active       - Faollik statusi (1=Faol, 0=Nofaol)
success_count   - Muvaffaqiyatli vazifalar
error_count     - Xatoga uchraydigan vazifalar
last_used       - Oxirgi ishlangan vaqt
created_at      - Yaratilgan vaqt
```

### `tasks` jadvali
```sql
id              - Vazifa ID
user_id         - Foydalanuvchi ID
account_id      - Akaunt ID (FOREIGN KEY)
task_data       - Vazifa ma'lumotlari (JSON)
status          - Status (PENDING, IN_PROGRESS, COMPLETED, FAILED, RETRY)
error_message   - Xato xabari
retry_count     - Qayta urinish soni
completed_at    - Tugallangan vaqt
created_at      - Yaratilgan vaqt
```

### `task_logs` jadvali (Xato kuzatish)
```sql
id              - Log ID
task_id         - Vazifa ID
account_id      - Akaunt ID
action          - Amal (Start execution, Button clicked, Subscribe, Confirm)
status          - Status (SUCCESS, ERROR, WAITING)
error           - Xato tafsili
created_at      - Yaratilgan vaqt
```

## 🎮 Bot Buyruqlari

| Buyruq | Tavsifi |
|--------|---------|
| `/start` | Botni ishga tushirish |
| `➕ Akaunt qo'shish` | Yangi Telegram akountni ulash |
| `📱 Akautlar` | Qo'shilgan akountlar ro'yxati |
| `📊 Statistika` | Vazifa statistikasi |
| `📝 Loglar` | Barcha loglar |

## ⚠️ Muammolar va Yechim

### ❌ "Module not found" xatosi
```bash
# Virtual muhit faol ekanligini tekshiring
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows

# Yana o'rnating
pip install -r requirements.txt
```

### ❌ "BOT_TOKEN not found"
```bash
# .env faylini tekshiring
cat .env  # Linux/Mac
type .env  # Windows

# .env.example dan .env ga ko'chirish
cp .env.example .env
```

### ❌ "2FA parol kerak" xatosi
Bot sessiya yaratishda 2FA parol kiritishni so'radi:
1. Terminal konsolida parol kiritishni kutib qoladi
2. OTP kodni kiriting va Enter bosing
3. Bot davom etadi

### ❌ Bot vazifani bajarava olmayapti
1. **Loglarni tekshiring:**
   ```bash
   tail -f data/logs.txt
   ```

2. **Ma'lumot bazasini tekshiring:**
   ```bash
   sqlite3 data/vazifachi.db ".schema"
   ```

3. **Xato xabarlari:**
   - Bot menusida 📝 Loglar tugmasini bosing
   - Xato detallari ko'rsatiladi

### ⚡ Bot juda sekin ishlamoqda
- `CONCURRENT_TASKS` qiymati ko'paytirilishi mumkin (config.py da)
- `RETRY_DELAY` qiymatini kamaytirish
- Internet tezligini tekshirish

## 🔧 Advanced Sozlamalar

### Timeout sozlash
```python
# config.py
TASK_TIMEOUT = 180  # 3 minutaga o'zgaritirish
```

### Qayta urinish soni
```python
RETRY_ATTEMPTS = 5  # 5 marta qayta urinish
RETRY_DELAY = 10    # 10 soniyadan keyin qayta urinish
```

### Parallel vazifalar soni
```python
CONCURRENT_TASKS = 10  # 10 ta vazifani bir vaqtda bajarilishi
```

## 📞 Yordam va Aloqa

Agar savol yoki xato bo'lsa:
- 🐛 **GitHub Issues** ga yozing
- 📧 **Admin bilan bog'lanish** uchun BotFather ga yozing
- 📝 **Loglar** dan xato tafsillarini ko'ring

## 📜 Litsenziya

Bu loyiha **MIT License** ostida tarqatiladi.

## 🙏 Xissa Qo'shish

Xissa qo'shishni istaysiz?
1. Loyihani fork qiling
2. Feature branch yarating (`git checkout -b feature/AmazingFeature`)
3. O'zgarishlarni commit qiling (`git commit -m 'Add some AmazingFeature'`)
4. Branch ga push qiling (`git push origin feature/AmazingFeature`)
5. Pull Request oching

---

**Vazifachi - Sizning Vazifalar, Bot Bajaradi!** 🚀

> Qo'shimcha savollar bo'lsa README ni o'qib chiqing yoki issues ga yozing.

**Muvaffaqiyati tilasiz!** ✨

---

**Oxirgi yangilanish:** 2026-06-09
**Versiya:** 2.0 (Multi-Account Support)
