import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import date

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "woodcraft_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///woodproducts.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

with app.app_context():
    import models
    import routes
    db.create_all()
    
    # Clear existing products
    from models import Product
    Product.query.delete()
    
    # Add sample products
    sample_products = [
        Product(
            name="ISPM 15 Certified Export Crates",
            description="International shipping standard compliant crates for export. Features heat treatment certification and proper IPPC marking.",
            category="Export Crates",
            image_url="/static/images/workshop.svg",
            price=0.0  # Quote based
        ),
        Product(
            name="Cushioned Crates",
            description="Custom-engineered crates with integrated cushioning systems for sensitive equipment protection.",
            category="Protective Packaging",
            image_url="/static/images/workshop.svg",
            price=0.0
        ),
        Product(
            name="Export Skidmates",
            description="Specialized skid systems designed for international shipping with integrated protection.",
            category="Export Solutions",
            image_url="/static/images/workshop.svg",
            price=0.0
        ),
        Product(
            name="Cushion Skids with Ramp",
            description="Heavy-duty skids with built-in ramp system and cushioning for easy loading and protection.",
            category="Industrial Skids",
            image_url="/static/images/workshop.svg",
            price=0.0
        ),
        Product(
            name="Oversize Crates",
            description="Custom-built oversized crating solutions for large industrial equipment and machinery.",
            category="Specialty Solutions",
            image_url="/static/images/workshop.svg",
            price=0.0
        )
    ]
    
    # Add sample testimonials if none exist
    from models import Testimonial
    if not Testimonial.query.first():
        sample_testimonials = [
            Testimonial(
                client_name="John D.",
                rating=5,
                content="Exceptional industrial packaging solutions! The custom crates perfectly protected our sensitive equipment during overseas shipping.",
                is_featured=True
            ),
            Testimonial(
                client_name="Sarah M.",
                rating=4,
                content="Their ISPM 15 certified export crates ensured smooth customs clearance. Great attention to international shipping requirements.",
                is_featured=True
            ),
            Testimonial(
                client_name="Michael R.",
                rating=5,
                content="The cushioned skids were perfect for our heavy machinery. Outstanding quality and professional service!",
                is_featured=True
            )
        ]
        for testimonial in sample_testimonials:
            db.session.add(testimonial)

    # Add sample gallery projects if none exist
    from models import GalleryProject
    if not GalleryProject.query.first():
        sample_projects = [
            GalleryProject(
                title="Custom Export Crate Solution",
                description="ISPM 15 certified export crates designed for sensitive medical equipment shipping to Europe. Features custom foam cushioning and moisture barriers.",
                image_url="/static/images/workshop.svg",
                completion_date=date(2024, 1, 15),
                client="MedTech Solutions",
                category="ISPM 15 Certified Export Crates",
                is_featured=True
            ),
            GalleryProject(
                title="Heavy Machinery Skids",
                description="Cushioned skids with integrated ramp system for 20-ton industrial equipment. Custom-engineered for repeated use and easy forklift access.",
                image_url="/static/images/workshop.svg",
                completion_date=date(2024, 2, 20),
                client="Industrial Dynamics",
                category="Cushion Skids with Ramp",
                is_featured=True
            ),
            GalleryProject(
                title="Oversized Crating Solution",
                description="Custom oversized crates for wind turbine components with specialized bracing and moisture control systems.",
                image_url="/static/images/workshop.svg",
                completion_date=date(2024, 3, 10),
                client="Green Energy Corp",
                category="Oversize Crates",
                is_featured=True
            ),
            GalleryProject(
                title="Reusable Shipping System",
                description="Developed a reusable crating system with Skidmates for regular international shipments, reducing packaging waste by 85%.",
                image_url="/static/images/workshop.svg",
                completion_date=date(2024, 4, 5),
                client="Global Electronics Ltd",
                category="Export with Skidmates",
                is_featured=True
            )
        ]
        for project in sample_projects:
            db.session.add(project)

    # Add the new sample products
    for product in sample_products:
        db.session.add(product)
        
    db.session.commit()
