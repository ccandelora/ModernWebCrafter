from functools import wraps
from flask import jsonify, current_app
import logging
from typing import Callable, Any

def setup_error_logging() -> None:
    """Configure error logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def handle_exceptions(f: Callable) -> Callable:
    """Decorator to handle exceptions in routes."""
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"Error in {f.__name__}: {str(e)}", exc_info=True)
            return jsonify({"error": "An internal error occurred"}), 500
    return wrapper

def log_route_access(route_name: str) -> Callable:
    """Decorator to log route access."""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_app.logger.info(f"Accessing route: {route_name}")
            return f(*args, **kwargs)
        return wrapper
    return decorator
