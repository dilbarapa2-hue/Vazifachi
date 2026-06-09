# Ma'lumot bazasi boshqaruvi
import sqlite3
import os
from datetime import datetime
from config import DATABASE_PATH

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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Vazifalar jadvali
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            account_id INTEGER NOT NULL,
            task_data TEXT NOT NULL,
            status TEXT DEFAULT 'PENDING',
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
            total_tasks INTEGER DEFAULT 0,
            completed_tasks INTEGER DEFAULT 0,
            failed_tasks INTEGER DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def add_account(user_id, phone_number, session_name):
    """Akaunt qo'shish"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO accounts (user_id, phone_number, session_name)
            VALUES (?, ?, ?)
        ''', (user_id, phone_number, session_name))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_accounts(user_id):
    """Foydalanuvchining akountlarini olish"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, phone_number, is_active, created_at
        FROM accounts
        WHERE user_id = ? AND is_active = 1
    ''', (user_id,))
    
    accounts = cursor.fetchall()
    conn.close()
    return accounts

def add_task(user_id, account_id, task_data):
    """Vazifa qo'shish"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO tasks (user_id, account_id, task_data, status)
        VALUES (?, ?, ?, 'PENDING')
    ''', (user_id, account_id, task_data))
    
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def get_pending_tasks(user_id):
    """Kutilmoqda bo'lgan vazifalarni olish"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, task_data, account_id
        FROM tasks
        WHERE user_id = ? AND status = 'PENDING'
        ORDER BY created_at ASC
    ''', (user_id,))
    
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task_status(task_id, status):
    """Vazifa statusini yangilash"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    completed_at = datetime.now() if status == 'COMPLETED' else None
    
    cursor.execute('''
        UPDATE tasks
        SET status = ?, completed_at = ?
        WHERE id = ?
    ''', (status, completed_at, task_id))
    
    conn.commit()
    conn.close()

def get_statistics(user_id):
    """Statistikani olish"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
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
        'failed': result[2] or 0
    }

def add_log(user_id, message):
    """Logga yozish"""
    os.makedirs(os.path.dirname(LOGS_PATH), exist_ok=True)
    
    with open(LOGS_PATH, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] User {user_id}: {message}\n")

def get_logs(user_id=None):
    """Loglarni olish"""
    if not os.path.exists(LOGS_PATH):
        return "Loglar mavjud emas"
    
    with open(LOGS_PATH, 'r', encoding='utf-8') as f:
        logs = f.readlines()
    
    if user_id:
        logs = [log for log in logs if f"User {user_id}" in log]
    
    return ''.join(logs[-50:]) if logs else "Loglar mavjud emas"
