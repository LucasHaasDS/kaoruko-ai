import sqlite3
from datetime import datetime

def create_database():
    connection = sqlite3.connect("kaoruko.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL,
            last_active TEXT NOT NULL
        )""")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        )""")

    connection.commit()
    connection.close()

def create_session(title):
    connection =sqlite3.connect("kaoruko.db")

    current_time = datetime.now().isoformat()

    cursor = connection.execute(
        """
        INSERT INTO sessions (title, created_at, last_active)
        VALUES (?, ?, ?)
        """,
        (title, current_time, current_time)
    )

    session_id = cursor.lastrowid
    
    connection.commit()
    connection.close()

    return session_id

def add_message(session_id, role, content):

    connection = sqlite3.connect("kaoruko.db")
    current_time = datetime.now().isoformat()

    connection.execute(
        """
        INSERT INTO messages (session_id, role, content, timestamp)
        VALUES (?, ?, ?, ?)
        """,
        (session_id, role, content, current_time)
    )

    connection.execute(
        """
        UPDATE sessions
        SET last_active = ?
        WHERE id = ?
        """,
        (current_time, session_id)
    )

    connection.commit()
    connection.close()

def get_messages(session_id):

    connection = sqlite3.connect("kaoruko.db")
    cursor = connection.execute(
        """
        SELECT role, content, timestamp
        FROM messages
        WHERE session_id = ?
        ORDER BY id ASC
        """,
        (session_id,)
    )

    messages = cursor.fetchall()
    connection.close()

    return messages

def get_sessions():

    connection = sqlite3.connect("kaoruko.db")

    cursor = connection.execute(
        """
        SELECT id, title, created_at, last_active
        FROM sessions
        ORDER BY last_active DESC
        """
    )

    sessions = cursor.fetchall()
    connection.close()

    return sessions

def get_latest_session():
    connection = sqlite3.connect("kaoruko.db")

    cursor = connection.execute(
        """
        SELECT id, title
        FROM sessions
        ORDER BY last_active DESC
        LIMIT 1
        """
    )

    session = cursor.fetchone()
    connection.close()

    return session

def update_session_activity(session_id):

    connection = sqlite3.connect("kaoruko.db")
    current_time = datetime.now().isoformat()

    connection.execute(
        """
        UPDATE sessions
        SET last_active = ?
        WHERE id = ?
        """,
        (current_time, session_id)
    )

    connection.commit()
    connection.close()

def rename_session(session_id, new_title):

    connection = sqlite3.connect("kaoruko.db")
    connection.execute(
        """
        UPDATE sessions
        SET title = ?
        WHERE id = ?
        """,
        (new_title, session_id)
    )

    connection.commit()
    connection.close()

def get_session_title(session_id):

    connection = sqlite3.connect("kaoruko.db")

    cursor = connection.execute(
        """
        SELECT title
        FROM sessions
        WHERE id = ?
        """,
        (session_id,)
    )

    result = cursor.fetchone()

    connection.close()
    
    if result is None:
        return None
    
    return result[0]