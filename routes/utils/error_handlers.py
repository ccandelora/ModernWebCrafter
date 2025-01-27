from functools import wraps
from flask import jsonify, current_app, render_template, request, flash, redirect, url_for
import logging
from typing import Callable, Any, Union
from flask import Response
import traceback
from flask_login import current_user

class ErrorHandler:
    """Error handling and logging configuration."""
    
    @staticmethod
    def init_app(app):
        """Initialize error handling for the application."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        @app.errorhandler(404)
        def not_found_error(error):
            current_app.logger.error(f'Page not found: {request.url}')
            return render_template('errors/404.html'), 404

        @app.errorhandler(500)
        def internal_error(error):
            current_app.logger.error('Server Error: %s', str(error))
            return render_template('errors/500.html'), 500

def handle_exceptions(f: Callable) -> Callable:
    """Enhanced decorator to handle exceptions in routes."""
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Union[Response, tuple]:
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_details = {
                'function': f.__name__,
                'error': str(e),
                'traceback': traceback.format_exc(),
                'user': current_user.username if not current_user.is_anonymous else 'anonymous',
                'endpoint': request.endpoint,
                'method': request.method,
                'url': request.url,
                'ip': request.remote_addr
            }
            
            current_app.logger.error(
                'Error in %(function)s: %(error)s\nUser: %(user)s\nEndpoint: %(endpoint)s\nMethod: %(method)s\nURL: %(url)s\nIP: %(ip)s\nTraceback:\n%(traceback)s',
                error_details
            )
            
            flash('An error occurred while processing your request. Please try again.', 'error')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"error": "An internal error occurred"}), 500
            
            # For admin routes, redirect to dashboard
            if request.endpoint and request.endpoint.startswith('admin.'):
                try:
                    return redirect(url_for('admin.dashboard'))
                except:
                    return render_template('errors/500.html'), 500
            
            return render_template('errors/500.html'), 500
    return wrapper

def log_route_access(route_name: str) -> Callable:
    """Enhanced decorator to log route access with request details."""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            access_details = {
                'route': route_name,
                'user': current_user.username if not current_user.is_anonymous else 'anonymous',
                'method': request.method,
                'url': request.url,
                'ip': request.remote_addr,
                'user_agent': request.user_agent.string
            }
            
            current_app.logger.info(
                'Route access: %(route)s\nUser: %(user)s\nMethod: %(method)s\nURL: %(url)s\nIP: %(ip)s\nUser Agent: %(user_agent)s',
                access_details
            )
            return f(*args, **kwargs)
        return wrapper
    return decorator
