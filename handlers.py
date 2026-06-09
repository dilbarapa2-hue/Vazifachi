# Telegram bot message handlers - Multi-account support
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from database import (
    add_account, get_accounts, get_pending_tasks, get_active_accounts,
    get_statistics, get_logs, add_log, disable_account
)
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Konversatsiya states
RECEIVE_PHONE = 1

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

<b>Asosiy Xususiyatlari:</b>
✅ Bir vaqtda 10 tagacha akount
🔄 5 ta vazifa parallel bajariladi
🛡️ Avtomatik xato tuzatish (3 urinish)
📊 To'liq statistika va loglar
⚡ Tez va ishonchli bajarilish

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
        await add_account_handler(query, user_id, context)
    elif query.data == "show_accounts":
        await show_accounts_handler(query, user_id)
    elif query.data == "statistics":
        await statistics_handler(query, user_id)
    elif query.data == "logs":
        await logs_handler(query, user_id)
    elif query.data == "back_to_menu":
        await query.edit_message_text(
            "<b>🏠 Asosiy Menyu</b>",
            reply_markup=get_main_menu(),
            parse_mode='HTML'
        )
    elif query.data.startswith("delete_account_"):
        account_id = int(query.data.split("_")[-1])
        await delete_account_handler(query, user_id, account_id)

async def add_account_handler(query, user_id, context):
    """Akaunt qo'shish"""
    add_log(user_id, "Akaunt qo'shish boshlandi")
    
    # Joriy akountlar sonini tekshirish
    accounts = get_accounts(user_id)
    if len(accounts) >= 10:
        await query.edit_message_text(
            "❌ <b>Maksimal 10 ta akaunt qo'shishingiz mumkin!</b>\n\n"
            f"Joriy: {len(accounts)}/10",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Asosiy menyu", callback_data="back_to_menu")]]),
            parse_mode='HTML'
        )
        return
    
    text = f"""
📱 <b>Akaunt qo'shish</b>

Iltimos, Telegram telefon raqamingizni kiriting:
(Masalan: +998901234567)

<b>Joriy akountlar:</b> {len(accounts)}/10
"""
    
    keyboard = [[InlineKeyboardButton("❌ Bekor qilish", callback_data="back_to_menu")]]
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )
    
    context.user_data['waiting_for_phone'] = True
    return RECEIVE_PHONE

async def receive_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Telefon raqamini qabul qilish"""
    user_id = update.effective_user.id
    phone = update.message.text.strip()
    
    if not context.user_data.get('waiting_for_phone'):
        return
    
    context.user_data['waiting_for_phone'] = False
    
    if not phone.startswith('+') or not phone[1:].isdigit():
        await update.message.reply_text(
            "❌ <b>Noto'g'ri format!</b>\n\n"
            "Iltimos, +998... formatida kiriting.",
            parse_mode='HTML'
        )
        return RECEIVE_PHONE
    
    # Akountni bazaga qo'shish
    session_name = f"session_{user_id}_{phone.replace('+', '')}"
    
    success, message = add_account(user_id, phone, session_name)
    
    if success:
        add_log(user_id, f"Akaunt qo'shildi: {phone}")
        
        text = f"""
✅ <b>Akaunt muvaffaqiyatli qo'shildi!</b>

📱 <b>Telefon:</b> <code>{phone}</code>
🔗 <b>Sessiya:</b> <code>{session_name}</code>

Ushbu akount orqali bot sizning vazifalarni avtomatik bajarib boradi.

⏳ <b>Birinchi urinishda 2FA parol kiritish talab qilinishi mumkin.</b>
"""
        
        keyboard = [[InlineKeyboardButton("🏠 Asosiy menyu", callback_data="back_to_menu")]]
        
        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
    else:
        await update.message.reply_text(
            f"❌ <b>Xato!</b>\n\n{message}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Asosiy menyu", callback_data="back_to_menu")]]),
            parse_mode='HTML'
        )
    
    return ConversationHandler.END

async def show_accounts_handler(query, user_id):
    """Akountlarni ko'rsatish"""
    add_log(user_id, "Akountlar ro'yxati ko'rildi")
    
    accounts = get_accounts(user_id)
    
    if not accounts:
        text = "📱 <b>Sizda hali akaunt yo'q</b>\n\nAkaunt qo'shish uchun ➕ tugmasini bosing."
        keyboard = [[InlineKeyboardButton("🏠 Asosiy menyu", callback_data="back_to_menu")]]
    else:
        text = f"📱 <b>Sizning akountlaringiz ({len(accounts)}/10):</b>\n\n"
        
        for idx, account in enumerate(accounts, 1):
            account_id, phone, is_active, success_count, error_count, last_used = account
            
            status = "✅ Faol" if is_active else "❌ Nofaol"
            stats = f"✅{success_count} ❌{error_count}"
            
            text += f"{idx}. {phone}\n   {status} | {stats}\n"
        
        keyboard = []
        for account in accounts:
            account_id = account[0]
            phone = account[1]
            keyboard.append([
                InlineKeyboardButton(f"❌ {phone}", callback_data=f"delete_account_{account_id}")
            ])
        
        keyboard.append([InlineKeyboardButton("🏠 Asosiy menyu", callback_data="back_to_menu")])
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

async def delete_account_handler(query, user_id, account_id):
    """Akountni o'chirish"""
    try:
        disable_account(account_id)
        add_log(user_id, f"Akaunt o'chirildi: {account_id}")
        
        await query.answer("✅ Akaunt o'chirildi", show_alert=True)
        await show_accounts_handler(query, user_id)
    except Exception as e:
        logger.error(f"Akaunt o'chirishda xato: {e}")
        await query.answer("❌ Xato yuz berdi", show_alert=True)

async def statistics_handler(query, user_id):
    """Statistikani ko'rsatish"""
    add_log(user_id, "Statistika ko'rildi")
    
    accounts = get_accounts(user_id)
    
    if not accounts:
        text = "📊 <b>Statistika mavjud emas</b>\n\nAkaunt qo'shing va vazifalar qo'shing."
    else:
        stats = get_statistics(user_id)
        
        text = f"""
📊 <b>Sizning Statistikangiz</b>

<b>Umumiy:</b>
📌 Jami vazifalar: {stats['total']}
✅ Tugallangan: {stats['completed']}
❌ Muvaffaqiyatsiz: {stats['failed']}
⏳ Kutilmoqda: {stats['pending']}

<b>Akountlar bo'yicha:</b>
"""
        for account in accounts:
            account_id, phone, is_active, success_count, error_count, last_used = account
            status = "✅" if is_active else "❌"
            text += f"\n{status} {phone}: ✅{success_count} | ❌{error_count}"
    
    keyboard = [[InlineKeyboardButton("🏠 Asosiy menyu", callback_data="back_to_menu")]]
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

async def logs_handler(query, user_id):
    """Loglarni ko'rsatish"""
    add_log(user_id, "Loglar ko'rildi")
    
    logs_text = get_logs(user_id, limit=30)
    
    if logs_text == "📝 Loglar mavjud emas":
        text = logs_text
    else:
        # Loglarni qisqartirish
        lines = logs_text.split('\n')
        limited_logs = '\n'.join(lines[-20:]) if len(lines) > 20 else logs_text
        text = f"""
📝 <b>Sizning Loglaringiz</b>

<code>{limited_logs}</code>
"""
    
    keyboard = [[InlineKeyboardButton("🏠 Asosiy menyu", callback_data="back_to_menu")]]
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xato handler"""
    logger.error(msg="Update caused error", exc_info=context.error)
    
    if update and update.effective_user:
        user_id = update.effective_user.id
        add_log(user_id, f"Bot xatosi: {context.error}")
