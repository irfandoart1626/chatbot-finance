# import mysql.connector
# from app.config import Config

# def get_db_connection():
#     return mysql.connector.connect(**Config.DB_CONFIG)

# def initialize_database():
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         telegram_id VARCHAR(50) UNIQUE NOT NULL,
#         created_at DATETIME DEFAULT CURRENT_TIMESTAMP
#     )
#     """)
    
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS transactions (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         telegram_id VARCHAR(50),
#         type ENUM('income', 'expense') NOT NULL,
#         amount INT NOT NULL,
#         description TEXT,
#         date DATETIME DEFAULT CURRENT_TIMESTAMP,
#         FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
#     )
#     """)
    
#     conn.commit()
#     cursor.close()
#     conn.close()


# def add_transaction(telegram_id, intent_type, amount, desc):
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     cursor.execute("INSERT INTO transactions (telegram_id, type, amount, description) VALUES (%s, %s, %s, %s)",
#                    (telegram_id, intent_type, amount, desc))
    
#     conn.commit()
#     cursor.close()
#     conn.close()


# def get_balance(telegram_id):
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
    
#     cursor.execute("""
#     SELECT SUM(CASE WHEN type='income' THEN amount ELSE -amount END) AS balance
#     FROM transactions WHERE telegram_id = %s
#     """, (telegram_id,))
    
#     result = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     return result['balance'] or 0


# def get_monthly_summary(telegram_id):
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
    
#     cursor.execute("""
#     SELECT 
#       SUM(CASE WHEN type='income' THEN amount ELSE 0 END) AS total_income,
#       SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) AS total_expense
#     FROM transactions WHERE telegram_id = %s AND date >= DATE_FORMAT(NOW(), '%Y-%m-01')
#     """, (telegram_id,))
    
#     result = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     return result








# import mysql.connector
# from app.config import Config


# def get_db_connection():
#     return mysql.connector.connect(**Config.DB_CONFIG)


# def initialize_database():
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         telegram_id VARCHAR(50) UNIQUE NOT NULL,
#         created_at DATETIME DEFAULT CURRENT_TIMESTAMP
#     )
#     """)

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS transactions (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         telegram_id VARCHAR(50),
#         type ENUM('income', 'expense') NOT NULL,
#         amount INT NOT NULL,
#         description TEXT,
#         date DATETIME DEFAULT CURRENT_TIMESTAMP,
#         FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
#     )
#     """)

#     conn.commit()
#     cursor.close()
#     conn.close()


# def register_user_if_not_exists(telegram_id):
#     """
#     Auto-register user jika belum terdaftar
#     """
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     try:
#         # Cek apakah user sudah ada
#         cursor.execute("SELECT telegram_id FROM users WHERE telegram_id = %s", (telegram_id,))
#         result = cursor.fetchone()

#         if not result:
#             # Jika belum ada, tambahkan user baru
#             cursor.execute("INSERT INTO users (telegram_id) VALUES (%s)", (telegram_id,))
#             conn.commit()
#             print(f"✅ User baru berhasil didaftarkan: {telegram_id}")
#     finally:
#         cursor.close()
#         conn.close()


# def add_transaction(telegram_id, intent_type, amount, desc):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     try:
#         # Pastikan user sudah terdaftar sebelum mencatat transaksi
#         register_user_if_not_exists(telegram_id)

#         # Simpan transaksi
#         cursor.execute(
#             "INSERT INTO transactions (telegram_id, type, amount, description) VALUES (%s, %s, %s, %s)",
#             (telegram_id, intent_type, amount, desc)
#         )
#         conn.commit()
#     finally:
#         cursor.close()
#         conn.close()


# def get_balance(telegram_id):
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)

#     try:
#         cursor.execute("""
#         SELECT SUM(CASE WHEN type='income' THEN amount ELSE -amount END) AS balance
#         FROM transactions WHERE telegram_id = %s
#         """, (telegram_id,))
#         result = cursor.fetchone()
#         return result['balance'] or 0
#     finally:
#         cursor.close()
#         conn.close()


# def get_monthly_summary(telegram_id):
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)

#     try:
#         cursor.execute("""
#         SELECT 
#           SUM(CASE WHEN type='income' THEN amount ELSE 0 END) AS total_income,
#           SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) AS total_expense
#         FROM transactions 
#         WHERE telegram_id = %s AND date >= DATE_FORMAT(NOW(), '%%Y-%%m-01')
#         """, (telegram_id,))
#         result = cursor.fetchone()
#         return result
#     finally:
#         cursor.close()
#         conn.close()




# import psycopg2
# from app.config import Config


# def get_db_connection():
#     return psycopg2.connect(**Config.DB_CONFIG)


# def initialize_database():
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id SERIAL PRIMARY KEY,  -- SERIAL untuk auto increment di PostgreSQL
#         telegram_id VARCHAR(50) UNIQUE NOT NULL,
#         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )
#     """)

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS transactions (
#         id SERIAL PRIMARY KEY,  -- SERIAL untuk auto increment di PostgreSQL
#         telegram_id VARCHAR(50),
#         type VARCHAR(10) CHECK (type IN ('income', 'expense')) NOT NULL,  -- VARCHAR dengan CHECK untuk ENUM di PostgreSQL
#         amount INT NOT NULL,
#         description TEXT,
#         date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#         FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
#     )
#     """)

#     conn.commit()
#     cursor.close()
#     conn.close()


# def register_user_if_not_exists(telegram_id):
#     """
#     Auto-register user jika belum terdaftar
#     """
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     try:
#         # Cek apakah user sudah ada
#         cursor.execute("SELECT telegram_id FROM users WHERE telegram_id = %s", (telegram_id,))
#         result = cursor.fetchone()

#         if not result:
#             # Jika belum ada, tambahkan user baru
#             cursor.execute("INSERT INTO users (telegram_id) VALUES (%s)", (telegram_id,))
#             conn.commit()
#             print(f"✅ User baru berhasil didaftarkan: {telegram_id}")
#     finally:
#         cursor.close()
#         conn.close()


# def add_transaction(telegram_id, intent_type, amount, desc):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     try:
#         # Pastikan user sudah terdaftar sebelum mencatat transaksi
#         register_user_if_not_exists(telegram_id)

#         # Simpan transaksi
#         cursor.execute(
#             "INSERT INTO transactions (telegram_id, type, amount, description) VALUES (%s, %s, %s, %s)",
#             (telegram_id, intent_type, amount, desc)
#         )
#         conn.commit()
#     finally:
#         cursor.close()
#         conn.close()


# def get_balance(telegram_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     try:
#         cursor.execute("""
#         SELECT SUM(CASE WHEN type='income' THEN amount ELSE -amount END) AS balance
#         FROM transactions WHERE telegram_id = %s
#         """, (telegram_id,))
#         result = cursor.fetchone()
#         return result['balance'] if result['balance'] is not None else 0
#     finally:
#         cursor.close()
#         conn.close()


# def get_monthly_summary(telegram_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     try:
#         cursor.execute("""
#         SELECT 
#             SUM(CASE WHEN type='income' THEN amount ELSE 0 END) AS total_income,
#             SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) AS total_expense
#         FROM transactions 
#         WHERE telegram_id = %s AND date >= DATE_TRUNC('month', CURRENT_DATE)
#         """, (telegram_id,))
#         result = cursor.fetchone()
#         return result
#     finally:
#         cursor.close()
#         conn.close()



import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import Config


def get_db_connection():
    """Membuat koneksi ke database menggunakan DATABASE_URL."""
    if not Config.DATABASE_URL:
        raise ValueError("DATABASE_URL tidak tersedia di environment variables.")
    
    return psycopg2.connect(
        Config.DATABASE_URL,
        cursor_factory=RealDictCursor
    )


def initialize_database():
    """Inisialisasi tabel jika belum ada."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id VARCHAR(50) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            telegram_id VARCHAR(50),
            type VARCHAR(10) CHECK (type IN ('income', 'expense')) NOT NULL,
            amount INT NOT NULL,
            description TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


def register_user_if_not_exists(telegram_id):
    """Mendaftarkan user ke tabel jika belum ada."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT telegram_id FROM users WHERE telegram_id = %s", (telegram_id,))
        result = cursor.fetchone()

        if not result:
            cursor.execute("INSERT INTO users (telegram_id) VALUES (%s)", (telegram_id,))
            conn.commit()
            print(f"✅ User baru berhasil didaftarkan: {telegram_id}")
    finally:
        cursor.close()
        conn.close()


def add_transaction(telegram_id, intent_type, amount, desc):
    """Menambahkan transaksi ke tabel transactions."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        register_user_if_not_exists(telegram_id)
        cursor.execute(
            "INSERT INTO transactions (telegram_id, type, amount, description) VALUES (%s, %s, %s, %s)",
            (telegram_id, intent_type, amount, desc)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_balance(telegram_id):
    """Mengembalikan total saldo user."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT SUM(CASE 
                WHEN type = 'income' THEN amount 
                ELSE -amount 
            END) AS balance
            FROM transactions
            WHERE telegram_id = %s
        """, (telegram_id,))
        result = cursor.fetchone()
        return result['balance'] if result['balance'] is not None else 0
    finally:
        cursor.close()
        conn.close()


def get_monthly_summary(telegram_id):
    """Mengembalikan ringkasan pemasukan dan pengeluaran bulan ini."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) AS total_income,
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS total_expense
            FROM transactions
            WHERE telegram_id = %s
              AND date >= DATE_TRUNC('month', CURRENT_DATE)
        """, (telegram_id,))
        result = cursor.fetchone()
        return {
            "total_income": result["total_income"] or 0,
            "total_expense": result["total_expense"] or 0
        }
    finally:
        cursor.close()
        conn.close()
