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
    "pool_pre_ping": True,
    "pool_recycle": 30,  # Recycle connections every 30 seconds for faster cleanup
    "pool_timeout": 3,   # Reduce timeout for faster failure detection
    "pool_size": 3,      # Minimal pool size for better resource usage
    "max_overflow": 1,   # Limited overflow to prevent resource exhaustion
    "connect_args": {
        "timeout": 3,     # Faster timeout for connection attempts
        "check_same_thread": False,
        "cached_statements": 10   # Further reduced statement cache for memory optimization
    }
}

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Import models at the top level
from models import Admin

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # type: ignore

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

def init_app():
    """Initialize the Flask application with optimized startup."""
    try:
        # Create instance directory if it doesn't exist
        if not os.path.exists('instance'):
            os.makedirs('instance', exist_ok=True)
            logger.info('Created instance directory')
        
        # Initialize database
        db.init_app(app)
        
        # Initialize database with retry logic
        from database import init_db_with_retry
        init_db_with_retry(app)
        
        # Initialize blueprints and error handlers
        with app.app_context():
            from routes import init_app as init_routes
            init_routes(app)
        
        logger.info('Application initialized successfully')
        return True
    except Exception as e:
        logger.error(f'Failed to initialize application: {str(e)}')
        raise

# Register cleanup handlers
@atexit.register
def cleanup():
    """Cleanup function to be called on application shutdown."""
    try:
        if hasattr(db, 'session'):
            db.session.remove()
        if hasattr(db, 'engine'):
            db.engine.dispose()
        logger.info("Database connections cleaned up successfully")
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")

if __name__ == '__main__':
    # Initialize the application
    init_app()
    
    # Initialize sample data
    try:
        from init_db import init_sample_data
        init_sample_data()
        logger.info("Sample data initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing sample data: {str(e)}")
    
    # Run the application
    app.run(host='0.0.0.0', port=5000)
