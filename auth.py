
import hashlib
import hmac
import sqlite3


DATABASE_NAME = "jobshield.db"


# Verify User Password
def verify_password(password, stored_hash):

    try:
        salt_hex, hash_hex = stored_hash.split("$")

        salt = bytes.fromhex(salt_hex)

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt,
            600000
        ).hex()

        return hmac.compare_digest(new_hash, hash_hex)

    except (ValueError, TypeError):
        return False


# User Login
def login_user(username, password):

    connection = None

    try:
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT password_hash
            FROM users
            WHERE username = ?
        """, (username,))

        user = cursor.fetchone()

        if user is None:
            return False

        stored_hash = user[0]

        return verify_password(password, stored_hash)

    except sqlite3.Error:
        return False

    finally:
        if connection is not None:
            connection.close()
