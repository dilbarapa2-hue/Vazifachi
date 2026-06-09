# Ma'lumot bazasi boshqaruvi - Multi-account support
import sqlite3
import os
from datetime import datetime
from config import DATABASE_PATH, LOGS_PATH
import json

def init_db():
    """Ma'lumot bazasini yaratish"""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Akountlar jadvali
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            phone_number TEXT UNIQUE NOT NULL,
            session_name TEXT,
            is_active BOOLEAN DEFAULT 1,
            last_used TIMESTAMP,
            error_count INTEGER DEFAULT 0,
            success_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Vazifalar jadvali
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            account_id INTEGER,
            task_data TEXT NOT NULL,
            status TEXT DEFAULT 'PENDING',
            error_message TEXT,
            retry_count INTEGER DEFAULT 0,
            completed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        )
    ''')
    
    # Statistika jadvali
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            account_id INTEGER NOT NULL,
            total_tasks INTEGER DEFAULT 0,
            completed_tasks INTEGER DEFAULT 0,
            failed_tasks INTEGER DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        )
    ''')
    
    # Task logs jadvali (xato tracking uchun)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            account_id INTEGER NOT NULL,
            action TEXT,
            status TEXT,
            error TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id),
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_account(user_id, phone_number, session_name):
    """Akaunt qo'shish (maksimal 10 ta)"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Joriy akountlar sonini tekshirish
        cursor.execute('''
            SELECT COUNT(*) FROM accounts 
            WHERE user_id = ? AND is_active = 1
        ''', (user_id,))
        
        count = cursor.fetchone()[0]
        
        if count >= 10:
            conn.close()
            return False, "❌ Maksimal 10 ta akaunt qo'shishingiz mumkin!"
        
        cursor.execute('''
            INSERT INTO accounts (user_id, phone_number, session_name)
            VALUES (?, ?, ?)
        ''', (user_id, phone_number, session_name))
        
        conn.commit()
        conn.close()
        return True, "✅ Akaunt muvaffaqiyatli qo'shildi!"
    except sqlite3.IntegrityError:
        return False, "❌ Bu telefon raqami allaqachon ro'yxatdan o'tgan!"
    except Exception as e:
        return False, f"❌ Xato: {str(e)}"

def get_accounts(user_id):
    """Foydalanuvchining akountlarini olish"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, phone_number, is_active, success_count, error_count, last_used
            FROM accounts
            WHERE user_id = ? AND is_active = 1
            ORDER BY created_at DESC
        ''', (user_id,))
        
        accounts = cursor.fetchall()
        conn.close()
        return accounts
    except Exception as e:
        print(f"Database error: {e}")
        return []

def get_active_accounts(user_id):
    """Faol akountlarini olish (vazifa bajarish uchun)"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, phone_number, session_name
            FROM accounts
            WHERE user_id = ? AND is_active = 1
            ORDER BY last_used ASC
            LIMIT 10
        ''', (user_id,))
        
        accounts = cursor.fetchall()
        conn.close()
        return accounts
    except Exception as e:
        print(f"Database error: {e}")
        return []

def update_account_status(account_id, success=True, error_message=None):
    """Akaunt statusini yangilash"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        if success:
            cursor.execute('''
                UPDATE accounts
                SET success_count = success_count + 1, 
                    error_count = 0,
                    last_used = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (account_id,))
        else:
            cursor.execute('''
                UPDATE accounts
                SET error_count = error_count + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (account_id,))
            
            # 3 ta xato bo'lsa akountni deaktiv qilish
            cursor.execute('SELECT error_count FROM accounts WHERE id = ?', (account_id,))
            error_count = cursor.fetchone()[0]
            
            if error_count >= 3:
                cursor.execute('UPDATE accounts SET is_active = 0 WHERE id = ?', (account_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False

def add_task(user_id, account_id, task_data):
    """Vazifa qo'shish"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        task_json = json.dumps(task_data) if isinstance(task_data, dict) else task_data
        
        cursor.execute('''
            INSERT INTO tasks (user_id, account_id, task_data, status)
            VALUES (?, ?, ?, 'PENDING')
        ''', (user_id, account_id, task_json))
        
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return task_id
    except Exception as e:
        print(f"Database error: {e}")
        return None

def get_pending_tasks(limit=5):
    """Kutilmoqda bo'lgan vazifalarni olish (concurrent limit bilan)"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, user_id, account_id, task_data
            FROM tasks
            WHERE status = 'PENDING'
            ORDER BY created_at ASC
            LIMIT ?
        ''', (limit,))
        
        tasks = cursor.fetchall()
        conn.close()
        return tasks
    except Exception as e:
        print(f"Database error: {e}")
        return []

def update_task_status(task_id, status, error_message=None):
    """Vazifa statusini yangilash"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        completed_at = datetime.now() if status == 'COMPLETED' else None
        
        cursor.execute('''
            UPDATE tasks
            SET status = ?, error_message = ?, completed_at = ?
            WHERE id = ?
        ''', (status, error_message, completed_at, task_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False

def increment_retry_count(task_id):
    """Qayta urinish sonini oshirish"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE tasks
            SET retry_count = retry_count + 1
            WHERE id = ?
        ''', (task_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False

def add_task_log(task_id, account_id, action, status, error=None):
    """Task logi qo'shish (xato tracking)"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO task_logs (task_id, account_id, action, status, error)
            VALUES (?, ?, ?, ?, ?)
        ''', (task_id, account_id, action, status, error))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False

def get_statistics(user_id, account_id=None):
    """Statistikani olish"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        if account_id:
            cursor.execute('''
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) as completed,
                    SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) as failed
                FROM tasks
                WHERE user_id = ? AND account_id = ?
            ''', (user_id, account_id))
        else:
            cursor.execute('''
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) as completed,
                    SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) as failed
                FROM tasks
                WHERE user_id = ?
            ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            'total': result[0] or 0,
            'completed': result[1] or 0,
            'failed': result[2] or 0,
            'pending': (result[0] or 0) - (result[1] or 0) - (result[2] or 0)
        }
    except Exception as e:
        print(f"Database error: {e}")
        return {'total': 0, 'completed': 0, 'failed': 0, 'pending': 0}

def add_log(user_id, message):
    """Logga yozish"""
    try:
        os.makedirs(os.path.dirname(LOGS_PATH), exist_ok=True)
        
        with open(LOGS_PATH, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] User {user_id}: {message}\n")
    except Exception as e:
        print(f"Log error: {e}")

def get_logs(user_id=None, limit=50):
    """Loglarni olish"""
    try:
        if not os.path.exists(LOGS_PATH):
            return "📝 Loglar mavjud emas"
        
        with open(LOGS_PATH, 'r', encoding='utf-8') as f:
            logs = f.readlines()
        
        if user_id:
            logs = [log for log in logs if f"User {user_id}" in log]
        
        return ''.join(logs[-limit:]) if logs else "📝 Loglar mavjud emas"
    except Exception as e:
        return f"❌ Log o'qishda xato: {e}"

def disable_account(account_id):
    """Akountni deaktiv qilish"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE accounts
            SET is_active = 0, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (account_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False
