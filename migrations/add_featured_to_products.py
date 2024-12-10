from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from app import db

def upgrade():
    # Add is_featured column to products table
    with current_app.app_context():
        db.engine.execute('ALTER TABLE product ADD COLUMN is_featured BOOLEAN DEFAULT FALSE')

def downgrade():
    # Remove is_featured column from products table
    with current_app.app_context():
        db.engine.execute('ALTER TABLE product DROP COLUMN is_featured') 