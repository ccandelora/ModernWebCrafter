import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import date
import json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
from flask import json

@app.template_filter('parse_json')
def parse_json_filter(value):
    try:
        return json.loads(value) if value else {}
    except:
        return {}

app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "woodcraft_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///woodproducts.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_timeout": 30,
    "connect_args": {"timeout": 15}
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

import time
import logging
from sqlalchemy.exc import OperationalError

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Import models at the top level
from models import Admin

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

def init_db_with_retry(max_retries=3, retry_delay=2):
    """Initialize database with retry logic."""
    retries = 0
    while retries < max_retries:
        try:
            with app.app_context():
                # Ensure instance folder exists
                if not os.path.exists('instance'):
                    os.makedirs('instance')
                    logger.info('Created instance directory')
                
                # Initialize database
                db.create_all()
                logger.info('Database initialized successfully')
                return True
        except OperationalError as e:
            retries += 1
            logger.warning(f'Database initialization attempt {retries} failed: {str(e)}')
            if retries < max_retries:
                time.sleep(retry_delay)
            else:
                logger.error('Database initialization failed after maximum retries')
                raise
        except Exception as e:
            logger.error(f'Unexpected error during database initialization: {str(e)}')
            raise

def init_app():
    """Initialize the Flask application."""
    try:
        # Initialize database
        db.init_app(app)
        
        # Initialize database with retry logic
        init_db_with_retry()
        
        # Register error handlers
        from routes.utils.error_handlers import ErrorHandler
        ErrorHandler.init_app(app)
        
        # Initialize routes
        from routes import init_app as init_routes
        init_routes(app)
        
        logger.info('Application initialized successfully')
    except Exception as e:
        logger.error(f'Failed to initialize application: {str(e)}')
        raise

# Initialize the application
init_app()

# Initialize sample data
try:
    from init_db import init_sample_data
    init_sample_data()
    logger.info("Sample data initialized successfully")
except Exception as e:
    logger.error(f"Error initializing sample data: {str(e)}")
