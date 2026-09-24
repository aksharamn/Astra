import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.getenv("ASTRA_SECRET_KEY") or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'astra.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ASTRA_MASTER_KEY = os.getenv("ASTRA_MASTER_KEY")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("ASTRA_COOKIE_SECURE", "0") == "1"
    MAX_CONTENT_LENGTH = 64 * 1024
    ASTRA_ALLOWED_ORIGINS = tuple(
        origin.strip()
        for origin in os.getenv("ASTRA_ALLOWED_ORIGINS", "http://localhost:5000,http://127.0.0.1:5000").split(",")
        if origin.strip()
    )
