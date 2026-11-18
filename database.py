
import sqlite3
from contextlib import contextmanager

DATABASE_NAME = "jobshield.db"


# Secure Database Connection
@contextmanager
def get_db_connection():

    connection = sqlite3.connect(DATABASE_NAME)

    try:
        # Enable SQLite foreign-key enforcement
        connection.execute("PRAGMA foreign_keys = ON")

        yield connection

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# Create Database and Tables
def create_database():

    with get_db_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_ad TEXT NOT NULL,
                risk_score INTEGER NOT NULL,
                risk_level TEXT NOT NULL
            )
        """)

        cursor.execute("PRAGMA table_info(scan_history)")
        columns = [column[1] for column in cursor.fetchall()]

        if "user_id" not in columns:
            cursor.execute("""
                ALTER TABLE scan_history
                ADD COLUMN user_id INTEGER REFERENCES users(id)
            """)


# Save Job Scan
def save_scan(job_ad, risk_score, risk_level, user_id):

    with get_db_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO scan_history
            (job_ad, risk_score, risk_level, user_id)
            VALUES (?, ?, ?, ?)
        """, (job_ad, risk_score, risk_level, user_id))


# Register New User
def register_user(username, email, password_hash):

    try:
        with get_db_connection() as connection:

            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            """, (username, email, password_hash))

        return True

    except sqlite3.IntegrityError:
        return False


# Get User ID
def get_user_id(username):

    with get_db_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT id FROM users
            WHERE username = ?
        """, (username,))

        result = cursor.fetchone()

        return result[0] if result else None


# Get User's Scan History
def get_scan_history(user_id):

    with get_db_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, job_ad, risk_score, risk_level
            FROM scan_history
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user_id,))

        return cursor.fetchall()


# Delete a Scan Belonging to a Specific User
def delete_scan(scan_id, user_id):

    with get_db_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM scan_history
            WHERE id = ? AND user_id = ?
        """, (scan_id, user_id))

        return cursor.rowcount


# Get User Profile
def get_user_profile(user_id):

    with get_db_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT username, email
            FROM users
            WHERE id = ?
        """, (user_id,))

        return cursor.fetchone()


# Update User Email
def update_user_email(user_id, new_email):

    try:
        with get_db_connection() as connection:

            cursor = connection.cursor()

            cursor.execute("""
                UPDATE users
                SET email = ?
                WHERE id = ?
            """, (new_email, user_id))

            return cursor.rowcount > 0

    except sqlite3.IntegrityError:
        return False


# Update User Password
def update_password_hash(user_id, new_password_hash):

    with get_db_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE users
            SET password_hash = ?
            WHERE id = ?
        """, (new_password_hash, user_id))

        return cursor.rowcount > 0


# Get Dashboard Statistics for a Specific User
def get_dashboard_stats(user_id):

    with get_db_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) AS total_scans,
                SUM(CASE WHEN risk_level = 'High Risk' THEN 1 ELSE 0 END),
                SUM(CASE WHEN risk_level = 'Medium Risk' THEN 1 ELSE 0 END),
                SUM(CASE WHEN risk_level = 'Low Risk' THEN 1 ELSE 0 END)
            FROM scan_history
            WHERE user_id = ?
        """, (user_id,))

        result = cursor.fetchone()

        return {
            "total": result[0] or 0,
            "high": result[1] or 0,
            "medium": result[2] or 0,
            "low": result[3] or 0
        }


# Check Database Tables
def check_tables():

    with get_db_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type = 'table'
        """)

        print("\nDatabase Tables:")

        for table in cursor.fetchall():
            print(table[0])

        cursor.execute("PRAGMA table_info(scan_history)")

        print("\nScan History Columns:")

        for column in cursor.fetchall():
            print(column[1])


# Run Database
if __name__ == "__main__":

    create_database()

    print("Karachi JobShield database is ready!")

    check_tables()
