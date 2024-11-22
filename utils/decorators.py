from functools import wraps
from flask import current_app, render_template

def log_route_access(route_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_app.logger.info(f'Access to {route_name}')
            return f(*args, **kwargs)
        return decorated_function
    return decorator 

def handle_exceptions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f'Error in {f.__name__}: {str(e)}')
            return render_template('errors/500.html'), 500
    return decorated_function 