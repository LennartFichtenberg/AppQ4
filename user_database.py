import sqlite3
import hashlib

DB_FILE = "users.db" # DB speicherort und name festlegen

# verbindung erstellen
def get_connection():
    return sqlite3.connect(DB_FILE)

# tabelle für "users" erstellem
def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            xp INTEGER NOT NULL DEFAULT 100
        )
    """)

    conn.commit()
    conn.close()

# passwort hashing definieren (hilfs funktion)
def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

"""Im folgenden stehen funktionen welche im backend verwendet werden um mit der DB zu kommunizieren"""

# nutzer hinzufügen
def add_user(name, password):
    conn = get_connection()
    cursor = conn.cursor()
    # passwwort hashen
    password_hash = hash_password(password)

    cursor.execute(
        "INSERT INTO users (name, password_hash, xp) VALUES (?, ?, ?)",
        (name, password_hash, 100)
    )

    conn.commit()
    conn.close()

# funktion welche für das einloggen im backend verwendet wird
def authenticate_user(name, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password_hash FROM users WHERE name = ?",
        (name,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return False

    return hash_password(password) == row[0]

# existenz prüfungs funktion
def user_exists(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM users WHERE name = ?",
        (name,)
    )

    row = cursor.fetchone()
    conn.close()

    return row is not None

# funktion zum nutzer auswählen
def get_user_xp(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT xp FROM users WHERE name = ?",
        (name,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return row[0]

# xp (währung) hinzufügen funktion
def add_xp(name, amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET xp = xp + ? WHERE name = ?",
        (amount, name)
    )

    conn.commit()
    conn.close()