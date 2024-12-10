import sqlite3
import os

def find_database():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    possible_locations = [
        os.path.join(current_dir, 'instance', 'woodproducts.db'),
        os.path.join(current_dir, 'woodproducts.db'),
        os.path.join(current_dir, 'instance', 'wood_products.db'),
        os.path.join(current_dir, 'wood_products.db'),
        'instance/woodproducts.db',
        'woodproducts.db',
        'instance/wood_products.db',
        'wood_products.db'
    ]
    
    for location in possible_locations:
        print(f"Checking location: {location}")
        if os.path.exists(location):
            print(f"Found database at: {location}")
            return location
            
    print("\nCurrent directory contents:")
    for item in os.listdir(current_dir):
        print(item)
    
    if os.path.exists('instance'):
        print("\nInstance directory contents:")
        for item in os.listdir('instance'):
            print(item)
            
    print("\nDatabase not found in any of the expected locations")
    return None

def add_featured_column():
    db_path = find_database()
    if not db_path:
        return
        
    try:
        # Connect to the database
        print("\nAttempting to connect to database...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Add the is_featured column
        print("Adding is_featured column...")
        try:
            cursor.execute('ALTER TABLE product ADD COLUMN is_featured BOOLEAN DEFAULT FALSE')
            conn.commit()
            print("Successfully added is_featured column")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("Column already exists, skipping")
            else:
                raise e
                
    except Exception as e:
        print(f"Error: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed")

if __name__ == "__main__":
    add_featured_column() 