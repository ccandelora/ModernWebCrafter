# This file makes the routes directory a Python package
from flask import Blueprint, current_app
from routes.utils.error_handlers import ErrorHandler

def init_app(app):
    """Initialize all routes and error handlers with enhanced error handling"""
    try:
        # Initialize error handlers first
        ErrorHandler.init_app(app)
        app.logger.debug('Error handlers initialized')
        
        # Import and register blueprints with error handling
        try:
            from routes.admin.routes import admin
            app.register_blueprint(admin)
            app.logger.debug('Admin blueprint registered')
        except Exception as e:
            app.logger.error(f'Failed to register admin blueprint: {str(e)}')
            raise

        try:
            from routes.auth.routes import auth
            app.register_blueprint(auth)
            app.logger.debug('Auth blueprint registered')
        except Exception as e:
            app.logger.error(f'Failed to register auth blueprint: {str(e)}')
            raise

        try:
            from routes.public.routes import public
            app.register_blueprint(public)
            app.logger.debug('Public blueprint registered')
        except Exception as e:
            app.logger.error(f'Failed to register public blueprint: {str(e)}')
            raise

        app.logger.info('All routes registered successfully')
        
    except Exception as e:
        app.logger.error(f'Failed to initialize routes: {str(e)}')
        raise
