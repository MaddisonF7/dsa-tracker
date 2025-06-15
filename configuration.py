# Import os
import os
# Import timedelta for session lifetime
from datetime import timedelta

# Configure MySQL database connection
class Config:
    # Dynamically retrives secret key from environment variable or uses a fallback value
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
    # CSRF protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.getenv('CSRF_SECRET_KEY', 'fallback-crsf-key')
    # MySQL database
    MYSQL_HOST = 'localhost'  # Change to host
    MYSQL_USER = 'root'  # Change to user
    MYSQL_PASSWORD = 'LilaDoodle0707!'  # Change to password
    MYSQL_DB = 'dsa_tracker'
    # Secure cookies sent over HTTPS
    SESSION_COOKIE_SECURE = True
    # Set session time 30mins
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
