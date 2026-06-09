# Telegram bot message handlers
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from database import (
    add_account, get_accounts, add_task, get_pending_tasks,
    update_task_status, get_statistics, get_logs, add_log
)
import json

# Main Menu
def get_main_menu():
    """Asosiy menyu tugmalarini olish"""
    keyboard = [
        [InlineKeyboardButton("➕ Akaunt qo'shish", callback_data="add_account")],
        [InlineKeyboardButton("📱 Akautlar", callback_data="show_accounts")],
        [InlineKeyboardButton("📊 Statistika", callback_data="statistics")],
        [InlineKeyboardButton("📝 Loglar", callback_data="logs")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start buyrug'i"""
    user_id = update.effective_user.id
    add_log(user_id, "Bot ishga tushirildi")
    
    welcome_text = """
👋 <b>Salom!</b>

Vazifachi botiga xush kelibsiz! 🤖

Bu bot sizga @Obunachi_X kanalining vazifalarini avtomatik bajarish imkoniyatini beradi.

<b>Quyidagilarni qila olasiz:</b>
✅ Telegram akountlarni qo'shish
📊 Statistikani ko'rish
📝 Loglarni tekshirish
🔄 Vazifalarni avtomatik bajarish

<b>Boshlash uchun tugmalardan birini tanlang:</b>
"""
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu(),
        parse_mode='HTML'
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tugma bosilganda"""
    query = update.callback_query
    user_id = query.from_user.id
    
    await query.answer()
    
    if query.data == "add_account":
        await add_account_handler(query, user_id)
    elif query.data == "show_accounts":
        await show_accounts_handler(query, user_id)
    elif query.data == "statistics":
        await statistics_handler(query, user_id)
    elif query.data == "logs":
        await logs_handler(query, user_id)
    elif query.data == "back_to_menu":
        await query.edit_message_text(
            "<b>Asosiy Menyu</b>",
            reply_markup=get_main_menu(),
            parse_mode='HTML'
        )

async def add_account_handler(query, user_id):
    """Akaunt qo'shish"""
    add_log(user_id, "Akaunt qo'shish boshlandi")
    
    text = """
📱 <b>Akaunt qo'shish</b>

Iltimos, Telegram telefon raqamingizni kiriting:
(Masalan: +998901234567)
"""
    
    keyboard = [[InlineKeyboardButton("❌ Bekor qilish", callback_data="back_to_menu")]]
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )
    
    # Kontekstga flag qo'shish
    from telegram.ext import ConversationHandler
    from handlers import receive_phone_number
    
    return "RECEIVE_PHONE"

async def receive_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Telefon raqamini qabul qilish"""
    user_id = update.effective_user.id
    phone = update.message.text.strip()
    
    if not phone.startswith('+'):
        await update.message.reply_text(
            "❌ Noto'g'ri format! Iltimos, +998... formatida kiriting."
        )
        return "RECEIVE_PHONE"
    
    # Akountni bazaga qo'shish
    session_name = f"session_{user_id}_{phone}"
    
    if add_account(user_id, phone, session_name):
        add_log(user_id, f"Akaunt qo'shildi: {phone}")
        
        text = f"""
✅ <b>Akaunt muvaffaqiyatli qo'shildi!</b>

📱 Telefon: <code>{phone}</code>

Ushbu akount orqali bot sizning vazifalarni avtomatik bajarib boradi.
"""
        
        keyboard = [[InlineKeyboardButton("🏠 Asosiy menyu", callback_data="back_to_menu")]]
        
        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
    else:
        await update.message.reply_text(
            "❌ Bu telefon raqami allaqachon ro'yxatdan o'tgan!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Asosiy menyu", callback_data="back_to_menu")]])
        )
    
    return ConversationHandler.END

async def show_accounts_handler(query, user_id):
    """Akountlarni ko'rsatish"""
    add_log(user_id, "Akountlar ro'yxati ko'rildi")
    
    accounts = get_accounts(user_id)
    
    if not accounts:
        text = "📱 <b>Sizda hali akaunt yo'q</b>\n\nAkaunt qo'shish uchun ➕ tugmasini bosing."
    else:
        text = "📱 <b>Sizning akountlaringiz:</b>\n\n"
        for idx, account in enumerate(accounts, 1):
            account_id, phone, is_active, created_at = account
            status = "✅ Faol" if is_active else "❌ Nofaol"
            text += f"{idx}. {phone} - {status}\n"
    
    keyboard = [[InlineKeyboardButton("🏠 Asosiy menyu", callback_data="back_to_menu")]]
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

async def statistics_handler(query, user_id):
    """Statistikani ko'rsatish"""
    add_log(user_id, "Statistika ko'rildi")
    
    stats = get_statistics(user_id)
    
    text = f"""
📊 <b>Sizning Statistikangiz</b>

📌 <b>Jami vazifalar:</b> {stats['total']}
✅ <b>Tugallangan:</b> {stats['completed']}
❌ <b>Muvaffaqiyatsiz:</b> {stats['failed']}
⏳ <b>Kutilmoqda:</b> {stats['total'] - stats['completed'] - stats['failed']}

<b>Bugungi sana:</b> Yangilanmoqda...
"""
    
    keyboard = [[InlineKeyboardButton("🏠 Asosiy menyu", callback_data="back_to_menu")]]
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

async def logs_handler(query, user_id):
    """Loglarni ko'rsatish"""
    add_log(user_id, "Loglar ko'rildi")
    
    logs_text = get_logs(user_id)
    
    text = f"""
📝 <b>Sizning Loglaringiz</b>

<code>{logs_text}</code>
"""
    
    keyboard = [[InlineKeyboardButton("🏠 Asosiy menyu", callback_data="back_to_menu")]]
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xato handler"""
    import logging
    logger = logging.getLogger(__name__)
    logger.error(msg="Update caused error", exc_info=context.error)
