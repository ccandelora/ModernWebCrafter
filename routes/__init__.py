# This file makes the routes directory a Python package
from flask import Blueprint, current_app
from routes.utils.error_handlers import ErrorHandler

def init_app(app):
    """Initialize all routes and error handlers with enhanced error handling"""
    try:
        # Initialize error handlers first
        ErrorHandler.init_app(app)
        
        # Import blueprints
        from routes.admin.routes import admin
        from routes.auth.routes import auth
        from routes.public.routes import public
        
        # Register blueprints in a single try block
        blueprints = [
            ('admin', admin),
            ('auth', auth),
            ('public', public)
        ]
        
        for name, blueprint in blueprints:
            try:
                app.register_blueprint(blueprint)
            except Exception as e:
                app.logger.error(f'Failed to register {name} blueprint: {str(e)}')
                raise

        app.logger.info('All routes registered successfully')
        
    except Exception as e:
        app.logger.error(f'Failed to initialize routes: {str(e)}')
        raise
