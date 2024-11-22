# This file makes the routes directory a Python package
from flask import Blueprint
from routes.admin.routes import admin
from routes.auth.routes import auth
from routes.public.routes import public
from routes.utils.error_handlers import ErrorHandler

def init_app(app):
    """Initialize all routes and error handlers"""
    # Register error handlers
    ErrorHandler.init_app(app)
    
    # Register blueprints
    app.register_blueprint(public)
    app.register_blueprint(admin)
    app.register_blueprint(auth)

    # Configure logging
    app.logger.info('All routes registered successfully')
