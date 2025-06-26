# Import os
import os
# Import url parse
from urllib.parse import urlparse
# Import timedelta for session lifetime
from datetime import timedelta


# Configure MySQL database connection
class Config:
    # Dynamically retrieves secret key
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
    # CSRF protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.getenv('CSRF_SECRET_KEY', 'fallback-crsf-key')

    # Default local MySQL
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'LilaDoodle0707!')
    MYSQL_DB = os.getenv('MYSQL_DB', 'dsa_tracker')

    # Override with JawsDB URL if set (Heroku environment)
    jawsdb_url = os.getenv('JAWSDB_URL')
    if jawsdb_url:
        url = urlparse(jawsdb_url)
        MYSQL_USER = url.username
        MYSQL_PASSWORD = url.password
        MYSQL_HOST = url.hostname
        MYSQL_DB = url.path.lstrip('/')

    # Secure cookies sent over HTTPS
    SESSION_COOKIE_SECURE = True
    # Set session time 30mins
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)


# Test configuration for unittests
class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'LilaDoodle0707!'
    MYSQL_DB = 'dsa_tracker_test'

    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'