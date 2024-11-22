import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import date
import json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

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

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # type: ignore

@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    return Admin.query.get(int(user_id))

db.init_app(app)
# Register error handlers
from routes.utils.error_handlers import ErrorHandler
ErrorHandler.init_app(app)

# Register blueprints
from routes.public.routes import public
from routes.admin.routes import admin
from routes.auth.routes import auth

app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(auth)

with app.app_context():
    import models
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
            image_url="/static/images/workshop.jpg",
            price=0.0  # Quote based
        ),
        Product(
            name="Cushioned Crates",
            description="Custom-engineered crates with integrated cushioning systems for sensitive equipment protection.",
            category="Protective Packaging",
            image_url="/static/images/workshop.jpg",
            price=0.0
        ),
        Product(
            name="Export Skidmates",
            description="Specialized skid systems designed for international shipping with integrated protection.",
            category="Export Solutions",
            image_url="/static/images/workshop.jpg",
            price=0.0
        ),
        Product(
            name="Cushion Skids with Ramp",
            description="Heavy-duty skids with built-in ramp system and cushioning for easy loading and protection.",
            category="Industrial Skids",
            image_url="/static/images/workshop.jpg",
            price=0.0
        ),
        Product(
            name="Oversize Crates",
            description="Custom-built oversized crating solutions for large industrial equipment and machinery.",
            category="Specialty Solutions",
            image_url="/static/images/workshop.jpg",
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

    # Clear and add updated gallery projects
    from models import GalleryProject
    GalleryProject.query.delete()
    
    sample_projects = [
        GalleryProject(
            title="Medical Equipment Export Package",
            description="ISPM 15 certified export crates designed for sensitive medical equipment shipping to Europe. Features custom foam cushioning and moisture barriers.",
            image_url="/static/images/workshop.jpg",
            completion_date=date(2024, 1, 15),
            completion_time=14,
            client="MedTech Solutions",
            category="ISPM 15 Certified Export Crates",
            industry_served="Medical Equipment",
            size_category="Large",
            weight_capacity="Up to 2,000 kg",
            ispm_compliant=True,
            special_features=json.dumps({
                "moisture_control": "Vapor barrier system",
                "cushioning": "Custom foam inserts",
                "monitoring": "Shock indicators installed"
            }),
            is_featured=True
        ),
        GalleryProject(
            title="Industrial Press Shipping Solution",
            description="Cushioned skids with integrated ramp system for 20-ton industrial equipment. Custom-engineered for repeated use and easy forklift access.",
            image_url="/static/images/workshop.jpg",
            completion_date=date(2024, 2, 20),
            completion_time=21,
            client="Industrial Dynamics",
            category="Cushion Skids with Ramp",
            industry_served="Manufacturing",
            size_category="Oversize",
            weight_capacity="Up to 20,000 kg",
            ispm_compliant=True,
            special_features=json.dumps({
                "ramp_system": "Integrated hydraulic ramp",
                "cushioning": "Heavy-duty shock absorption",
                "reusability": "Designed for 10+ uses"
            }),
            is_featured=True
        ),
        GalleryProject(
            title="Wind Turbine Component Package",
            description="Custom oversized crates for wind turbine components with specialized bracing and moisture control systems.",
            image_url="/static/images/workshop.jpg",
            completion_date=date(2024, 3, 10),
            completion_time=30,
            client="Green Energy Corp",
            category="Specialty/Oversize Solutions",
            industry_served="Renewable Energy",
            size_category="Oversize",
            weight_capacity="Up to 15,000 kg",
            ispm_compliant=True,
            special_features=json.dumps({
                "bracing": "Custom steel reinforcement",
                "moisture_control": "Active dehumidification",
                "monitoring": "GPS tracking system"
            }),
            is_featured=True
        ),
        GalleryProject(
            title="Electronics Reusable Export System",
            description="Developed a reusable crating system with Skidmates for regular international shipments, reducing packaging waste by 85%.",
            image_url="/static/images/workshop.jpg",
            completion_date=date(2024, 4, 5),
            completion_time=25,
            client="Global Electronics Ltd",
            category="Export with Skidmates",
            industry_served="Electronics",
            size_category="Medium",
            weight_capacity="Up to 5,000 kg",
            ispm_compliant=True,
            special_features=json.dumps({
                "reusability": "100+ use cycle",
                "cushioning": "Modular foam system",
                "security": "Tamper-evident seals"
            }),
            is_featured=True
        )
    ]

    # Add the sample projects
    for project in sample_projects:
        db.session.add(project)

    # Add the sample products
    for product in sample_products:
        db.session.add(product)
        
    db.session.commit()
    # Add sample team members if none exist
    from models import TeamMember
    if not TeamMember.query.first():
        sample_team = [
            TeamMember(
                name="John Smith",
                role="CEO & Founder",
                bio="30+ years of expertise in custom industrial packaging solutions and international shipping.",
                order=1,
                is_active=True
            ),
            TeamMember(
                name="Sarah Johnson",
                role="Operations Director",
                bio="25+ years of manufacturing and industrial packaging operations expertise.",
                order=2,
                is_active=True
            ),
            TeamMember(
                name="Michael Brown",
                role="Engineering Manager",
                bio="20+ years of custom wood crating and export packaging design experience.",
                order=3,
                is_active=True
            )
        ]
        for member in sample_team:
            db.session.add(member)

