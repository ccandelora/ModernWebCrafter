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
        db.session.commit()

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
        db.session.commit()
