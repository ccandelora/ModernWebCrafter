from app import app, db
from models import Admin

def create_admin():
    try:
        # First, check if admin user exists and delete if it does
        admin = Admin.query.filter_by(username='admin').first()
        if admin:
            db.session.delete(admin)
            db.session.commit()
            print("Existing admin user deleted")
        
        # Create new admin user
        admin = Admin()
        admin.username = 'admin'
        admin.email = 'admin@example.com'
        admin.set_password('centrifugal')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
        return True
    except Exception as e:
        print(f"Error creating admin user: {str(e)}")
        return False

if __name__ == "__main__":
    with app.app_context():
        create_admin()
