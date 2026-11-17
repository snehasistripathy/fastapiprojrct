
import os
from pathlib import Path
from dotenv import load_dotenv

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Load environment variables
load_dotenv(BASE_DIR / ".env")


# --------------------------------------------------
# Application configuration
# --------------------------------------------------

APP_NAME = os.getenv(
    "APP_NAME",
    "Student Management API"
)

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

API_V1_PREFIX = os.getenv(
    "API_V1_PREFIX",
    "/api/v1"
)


# --------------------------------------------------
# Database configuration
# --------------------------------------------------

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_SSLMODE = os.getenv("DB_SSLMODE", "verify-full")

DB_SSLROOTCERT = os.getenv(
    "DB_SSLROOTCERT",
    "./global-bundle.pem"
)

# Construct asynchronous PostgreSQL URL
DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    if all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD])
    else None
)


# --------------------------------------------------
# JWT configuration
# --------------------------------------------------

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)


# --------------------------------------------------
# Validate required variables
# --------------------------------------------------

required_variables = {
    "DB_HOST": DB_HOST,
    "DB_NAME": DB_NAME,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "SECRET_KEY": SECRET_KEY
}

missing_variables = [
    key for key, value in required_variables.items()
    if not value
]

if missing_variables:
    raise ValueError(
        f"Missing environment variables: {', '.join(missing_variables)}"
    )
