# Import Flask for creating web application
from flask import Flask, session
# Import MySQL to connect to MySQL database
from flask_mysqldb import MySQL
# Import CSRF protection extension
from flask_wtf import CSRFProtect
# Import talisman for security headers
from flask_talisman import Talisman
# Import the Config class to load MySQL database from configuration.py
from configuration import Config

# Create a MySQL instance
mysql = MySQL()
# Create a CSRFProtect instance
csrf = CSRFProtect()


# create_app function
def create_app():
    # Create a Flask instance
    app = Flask(__name__)
    # Load configurations from Config class for MySQL connection
    app.config.from_object(Config)
    # Initialise MySQL connection to Flask app
    mysql.init_app(app)
    # Initialise CSRF protection to Flask app
    csrf.init_app(app)
    # Setup Talisman security headers
    Talisman(
        app,
        content_security_policy={
            # From own domain
            'default-src': ["'self"],
        },
        # Send cookies over HTTPS
        session_cookie_secure=True,
        # Prevent JS access to cookies
        session_cookie_http_only=True,
        # Protect against CSRF
        session_cookie_samesite='Lax'
    )

    # Set session to be permanent 30mins
    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = (
            app.config['PERMANENT_SESSION_LIFETIME']
        )
        
    # Import blueprint for routes
    from routes import main_bp
    # Register blueprint's routes
    app.register_blueprint(main_bp)
    return app
