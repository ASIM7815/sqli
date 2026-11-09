import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).parent
INSTANCE_DIR = BASE_DIR / "instance" / "data"
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        import warnings
        warnings.warn(
            "SECRET_KEY not set in environment. Using a random key for this session. "
            "Set SECRET_KEY in production or for persistent sessions.",
            RuntimeWarning
        )
        SECRET_KEY = secrets.token_hex(32)

    DATABASE_PATH = INSTANCE_DIR / "sqli_lab.db"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "0") == "1"
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 3600

    FLAG = os.environ.get("CTF_FLAG", "CTF{legacy_query_exposed}")

    @staticmethod
    def init_app(app):
        pass