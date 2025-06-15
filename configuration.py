# Import os
import os
# Import timedelta for session lifetime
from datetime import timedelta


# Configure MySQL database connection
class Config:
    # Dynamically retrives secret key
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
    # CSRF protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.getenv('CSRF_SECRET_KEY', 'fallback-crsf-key')
    # MySQL database
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', '')

    # Secure cookies sent over HTTPS
    SESSION_COOKIE_SECURE = True
    # Set session time 30mins
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
