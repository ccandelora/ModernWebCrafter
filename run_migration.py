from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import importlib.util
import os

def run_migration(migration_file):
    # Create a minimal Flask application
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/woodproducts.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db = SQLAlchemy(app)
    
    # Import the migration module
    spec = importlib.util.spec_from_file_location(
        "migration", 
        os.path.join("migrations", migration_file)
    )
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    
    with app.app_context():
        try:
            # Run the upgrade using raw SQL
            db.session.execute('ALTER TABLE product ADD COLUMN is_featured BOOLEAN DEFAULT FALSE')
            db.session.commit()
            print(f"Successfully ran migration: {migration_file}")
        except Exception as e:
            db.session.rollback()
            if "duplicate column name" in str(e).lower():
                print("Column already exists, skipping migration")
            else:
                print(f"Error running migration: {str(e)}")

if __name__ == "__main__":
    run_migration("add_featured_to_products.py") 