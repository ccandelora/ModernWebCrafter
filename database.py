from flask_sqlalchemy import SQLAlchemy
import logging
import time
from sqlalchemy.exc import OperationalError

# Configure logging
logger = logging.getLogger(__name__)

# Initialize SQLAlchemy
db = SQLAlchemy()

def init_db_with_retry(app, max_retries=3, retry_delay=2):
    """Initialize database with optimized retry logic."""
    retries = 0
    while retries < max_retries:
        try:
            with app.app_context():
                # Initialize database with fast_executemany for better performance
                with db.engine.connect() as conn:
                    conn.execute(db.text('PRAGMA journal_mode=WAL'))  # Use WAL mode for better concurrency
                db.create_all()
                logger.info('Database initialized successfully')
                return True
        except OperationalError as e:
            retries += 1
            logger.warning(f'Database initialization attempt {retries} failed: {str(e)}')
            if retries < max_retries:
                time.sleep(retry_delay * retries)  # Exponential backoff
            else:
                logger.error('Database initialization failed after maximum retries')
                raise
        except Exception as e:
            logger.error(f'Unexpected error during database initialization: {str(e)}')
            raise
