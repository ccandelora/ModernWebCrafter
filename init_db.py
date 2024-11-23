from app import create_app
from extensions import db
from models import User, Product, Testimonial

def init_db():
    app = create_app()
    with app.app_context():
        # Drop and recreate all tables
        db.drop_all()
        db.create_all()

        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin_user.set_password('admin123')  # Set a secure password in production!
        db.session.add(admin_user)

        # Add sample testimonials
        testimonials = [
            Testimonial(
                client_name="John Doe",
                content="Excellent quality and service!",
                rating=5,
                is_featured=True
            ),
            Testimonial(
                client_name="Jane Smith",
                content="Very professional team. They delivered exactly what we needed for our international shipping.",
                rating=5,
                is_featured=True
            ),
            Testimonial(
                client_name="Bob Johnson",
                content="Great attention to detail and excellent customer service.",
                rating=4,
                is_featured=True
            )
        ]
        
        # Add sample products
        products = [
            Product(
                name="Export Crate",
                category="Shipping",
                description="ISPM-15 compliant export crating solution",
                image_url="/static/images/products/export-crate.jpg"
            ),
            Product(
                name="Custom Skid",
                category="Industrial",
                description="Heavy-duty custom skid for industrial equipment",
                image_url="/static/images/products/custom-skid.jpg"
            ),
            Product(
                name="Protective Packaging",
                category="Specialty",
                description="Custom protective packaging solutions",
                image_url="/static/images/products/protective-packaging.jpg"
            )
        ]
        
        # Add all samples to database
        db.session.add_all(testimonials)
        db.session.add_all(products)
        
        # Commit changes
        db.session.commit()
        print("Database initialized with sample data!")

if __name__ == "__main__":
    init_db() 