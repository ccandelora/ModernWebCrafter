import os
import logging
from flask import Flask
from extensions import init_extensions, db, login_manager
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Basic configuration from environment variables
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Add custom template filters
    @app.template_filter('to_json')
    def to_json_filter(value):
        try:
            return json.loads(value) if value else {}
        except (ValueError, TypeError):
            return {}
    
    @app.template_filter('parse_json')
    def parse_json_filter(value):
        try:
            if isinstance(value, dict):
                return value
            return json.loads(value) if value else {}
        except (ValueError, TypeError):
            return {}
    
    # Initialize extensions
    init_extensions(app)
    
    # Register error handlers
    try:
        from routes.utils.error_handlers import ErrorHandler
        ErrorHandler.init_app(app)
        app.logger.info('Error handlers initialized successfully')
    except Exception as e:
        app.logger.error(f'Failed to initialize error handlers: {str(e)}')
        raise

    # Initialize routes
    try:
        from routes import init_app as init_routes
        init_routes(app)
        app.logger.info('Routes initialized successfully')
    except Exception as e:
        app.logger.error(f'Failed to initialize routes: {str(e)}')
        raise
    
    return app

# Create the application instance
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    return Admin.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)
