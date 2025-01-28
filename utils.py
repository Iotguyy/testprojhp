import bcrypt
import jwt as pyjwt
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Hash password
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Create JWT Token
def create_access_token(data: dict, expires_delta: datetime.timedelta):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return pyjwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 