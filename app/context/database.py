import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = "data/context.db"
NEON_DATABASE_URL = os.getenv("NEON_DATABASE_URL")


def get_connection():
    """Use Neon PostgreSQL when configured; otherwise use local SQLite."""
    if NEON_DATABASE_URL:
        import psycopg

        return psycopg.connect(NEON_DATABASE_URL)

    os.makedirs("data", exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
def execute_query(cursor, query, params=()):
    """Execute SQL using the placeholder syntax required by the database."""
    if NEON_DATABASE_URL:
        query = query.replace("?", "%s")

    cursor.execute(query, params)
    return cursor

def initialize_database():
    """Initialize tables for local SQLite development only."""
    if NEON_DATABASE_URL:
        # Neon tables were created and populated by the migration script.
        # Do not recreate or modify the production schema automatically.
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE NOT NULL,
            target_role TEXT,
            experience_level TEXT,
            skills TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE NOT NULL,
            remote_only INTEGER DEFAULT 0,
            preferred_locations TEXT,
            preferred_skills TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            job_id TEXT NOT NULL,
            title TEXT,
            job_url TEXT,
            status TEXT DEFAULT 'saved',
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            applied_at TIMESTAMP,
            UNIQUE(user_id, job_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            job_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    connection.commit()
    connection.close()