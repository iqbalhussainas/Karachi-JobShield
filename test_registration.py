import os
import hashlib
import secrets

from dotenv import load_dotenv
from database import register_user

load_dotenv()

# Test user details
username = "test_user_02"
email = "test02@example.com"
password = os.getenv("JOBSHIELD_TEST_PASSWORD")

if not password:
    raise RuntimeError("JOBSHIELD_TEST_PASSWORD is missing from .env")

# Generate a secure password hash
salt = secrets.token_bytes(16)

password_hash = (
    salt.hex() + "$" +
    hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        600000
    ).hex()
)

# Register user
result = register_user(username, email, password_hash)

if result:
    print("User registered successfully!")
else:
    print("Registration failed: Username or email already exists.")