import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY", "super_secret_key_123")

DEBUG = os.environ.get("DEBUG", False)

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    os.environ.get("ALLOWED_HOSTS", "*"),
]

if os.environ.get("DB_ENGINE"):
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("DB_ENGINE"),
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "db.sqlite3",
        }
    }

TIME_ZONE = os.environ.get("TIME_ZONE", "UTC")

DEFAULT_ANONUMOUS_USER_PASSWORD = "anonymous_user"
