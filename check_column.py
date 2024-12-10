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

def check_column():
    db_path = find_database()
    if not db_path:
        return
        
    try:
        # Connect to the database
        print("\nAttempting to connect to database...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get table info
        print("Checking table structure...")
        cursor.execute("PRAGMA table_info(product)")
        columns = cursor.fetchall()
        print("\nAll columns in product table:")
        for col in columns:
            print(f"Column: {col[1]}, Type: {col[2]}")
        
        # Check for is_featured column
        is_featured_exists = any(col[1] == 'is_featured' for col in columns)
        
        if is_featured_exists:
            print("\nThe is_featured column exists in the product table")
            # Show some sample data
            print("\nFetching sample data...")
            cursor.execute("SELECT id, name, is_featured FROM product LIMIT 5")
            rows = cursor.fetchall()
            print("\nSample data:")
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Featured: {row[2]}")
        else:
            print("\nThe is_featured column does not exist in the product table")
                
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("\nDatabase connection closed")

if __name__ == "__main__":
    check_column() 