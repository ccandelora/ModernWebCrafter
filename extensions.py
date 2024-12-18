from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from sqlalchemy.orm import DeclarativeBase
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# Initialize Flask-Mail with deferred app initialization
mail = Mail()

def create_mail_instance(app):
    """Create a new Flask-Mail instance with the given app"""
    try:
        app.logger.info('Configuring Flask-Mail...')
        
        # Mail server settings
        app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
        app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
        app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
        app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
        app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
        app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
        app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
        
        # Additional settings for debugging
        app.config['MAIL_DEBUG'] = True
        app.config['MAIL_SUPPRESS_SEND'] = False
        app.config['TESTING'] = False
        app.config['MAIL_MAX_EMAILS'] = None
        app.config['MAIL_ASCII_ATTACHMENTS'] = False
        
        # Log mail configuration (excluding password)
        app.logger.info('Mail Configuration:')
        app.logger.info(f'MAIL_SERVER: {app.config["MAIL_SERVER"]}')
        app.logger.info(f'MAIL_PORT: {app.config["MAIL_PORT"]}')
        app.logger.info(f'MAIL_USE_TLS: {app.config["MAIL_USE_TLS"]}')
        app.logger.info(f'MAIL_USE_SSL: {app.config["MAIL_USE_SSL"]}')
        app.logger.info(f'MAIL_USERNAME: {app.config["MAIL_USERNAME"]}')
        app.logger.info(f'MAIL_DEFAULT_SENDER: {app.config["MAIL_DEFAULT_SENDER"]}')
        
        # Create and initialize a new Mail instance
        mail_instance = Mail(app)
        app.logger.info('Flask-Mail initialized successfully')
        return mail_instance
        
    except Exception as e:
        app.logger.error(f'Error configuring Flask-Mail: {str(e)}')
        raise

def init_extensions(app):
    """Initialize all Flask extensions"""
    try:
        # Initialize database
        db.init_app(app)
        app.logger.info('Database initialized successfully')
        
        # Initialize login manager
        login_manager.init_app(app)
        login_manager.login_view = 'auth.login'
        app.logger.info('Login manager initialized successfully')
        
        # Initialize mail
        global mail
        mail = create_mail_instance(app)
        app.logger.info('Mail extension initialized successfully')
        
    except Exception as e:
        app.logger.error(f'Error initializing extensions: {str(e)}')
        raise