import os
from dotenv import load_dotenv
from auth import login_user

load_dotenv()

username = "test_user_02"
password = os.getenv("JOBSHIELD_TEST_PASSWORD")

if not password:
    raise RuntimeError("JOBSHIELD_TEST_PASSWORD is missing from .env")


# Test correct login
result = login_user(username, password)

if result:
    print("Login successful!")
else:
    print("Invalid username or password!")


# Test incorrect password
wrong_password = "DefinitelyWrongPassword123"

result = login_user(username, wrong_password)

if result:
    print("Login successful!")
else:
    print("Invalid username or password!")