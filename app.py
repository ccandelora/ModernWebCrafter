import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

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
