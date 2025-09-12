import os

LOG_DB_USER = os.getenv("LOG_DB_USER", "log_user")
LOG_DB_PASS = os.getenv("LOG_DB_PASS", "log_pass")
LOG_DB_HOST = os.getenv("LOG_DB_HOST", "log-db")
LOG_DB_PORT = os.getenv("LOG_DB_PORT", "3306")
LOG_DB_NAME = os.getenv("LOG_DB_NAME", "log_db")

DATABASE_URL = (
    f"mysql+pymysql://{LOG_DB_USER}:{LOG_DB_PASS}@{LOG_DB_HOST}:{LOG_DB_PORT}/{LOG_DB_NAME}?charset=utf8mb4"
)