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
                content="Exceptional craftsmanship! The custom dining table they made exceeded our expectations.",
                is_featured=True
            ),
            Testimonial(
                client_name="Sarah M.",
                rating=4,
                content="Beautiful work on our kitchen cabinets. The attention to detail is remarkable.",
                is_featured=True
            ),
            Testimonial(
                client_name="Michael R.",
                rating=5,
                content="The handcrafted bookshelf is a piece of art. Fantastic quality and service!",
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
                title="Custom Dining Room Set",
                description="A complete dining room set including a table for 8, chairs, and a matching sideboard. Made from solid oak with a natural finish.",
                image_url="/static/images/workshop.svg",
                completion_date=date(2024, 1, 15),
                client="Smith Family",
                category="Furniture Sets",
                is_featured=True
            ),
            GalleryProject(
                title="Modern Kitchen Cabinets",
                description="Full kitchen renovation with custom maple cabinets featuring soft-close drawers and built-in organizers.",
                image_url="/static/images/workshop.svg",
                completion_date=date(2024, 2, 20),
                client="Johnson Residence",
                category="Kitchen",
                is_featured=True
            ),
            GalleryProject(
                title="Built-in Library Shelving",
                description="Floor-to-ceiling library shelving with a rolling ladder, crafted from walnut with adjustable shelves.",
                image_url="/static/images/workshop.svg",
                completion_date=date(2024, 3, 10),
                client="City Library",
                category="Storage Solutions",
                is_featured=True
            ),
            GalleryProject(
                title="Outdoor Deck Furniture",
                description="Weather-resistant teak furniture set including loungers, dining set, and storage boxes.",
                image_url="/static/images/workshop.svg",
                completion_date=date(2024, 4, 5),
                client="Beach House Resort",
                category="Outdoor",
                is_featured=False
            )
        ]
        for project in sample_projects:
            db.session.add(project)
        db.session.commit()
