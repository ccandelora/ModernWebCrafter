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
from flask import json
from flask import json
import datetime

def custom_json_encoder(obj):
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError(f'Object of type {type(obj)} is not JSON serializable')

app.json.encoder = custom_json_encoder

@app.template_filter('parse_json')
def parse_json_filter(value):
    try:
        return json.loads(value) if value else {}
    except:
        return {}

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


import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize database
db.init_app(app)

# Register error handlers
try:
    from routes.utils.error_handlers import ErrorHandler
    ErrorHandler.init_app(app)
    app.logger.info('Error handlers initialized successfully')
except Exception as e:
    app.logger.error(f'Failed to initialize error handlers: {str(e)}')
    raise

# Initialize routes with error handling
try:
    from routes import init_app
    init_app(app)
    app.logger.info('Routes initialized successfully')
except Exception as e:
    app.logger.error(f'Failed to initialize routes: {str(e)}')
    raise

# Database initialization with error handling
try:
    with app.app_context():
        import models
        # Ensure instance folder exists
        import os
        if not os.path.exists('instance'):
            os.makedirs('instance')
            app.logger.info('Created instance directory')

        db.create_all()
        app.logger.info('Database initialized successfully')

        # Import models for sample data
        from models import Product, Testimonial, GalleryProject, TeamMember
        
        app.logger.info('Starting sample data population checks...')

        # Sample products data
        sample_products = [
            Product(**{
                'name': "ISPM 15 Certified Export Crates",
                'description': "International shipping standard compliant crates for export. Features heat treatment certification and proper IPPC marking.",
                'category': "Export Crates",
                'image_url': "/static/images/workshop.jpg",
                'price': 0.0  # Quote based
            }),
            Product(**{
                'name': "Cushioned Crates",
                'description': "Custom-engineered crates with integrated cushioning systems for sensitive equipment protection.",
                'category': "Protective Packaging",
                'image_url': "/static/images/workshop.jpg",
                'price': 0.0
            }),
            Product(**{
                'name': "Export Skidmates",
                'description': "Specialized skid systems designed for international shipping with integrated protection.",
                'category': "Export Solutions",
                'image_url': "/static/images/workshop.jpg",
                'price': 0.0
            }),
            Product(**{
                'name': "Cushion Skids with Ramp",
                'description': "Heavy-duty skids with built-in ramp system and cushioning for easy loading and protection.",
                'category': "Industrial Skids",
                'image_url': "/static/images/workshop.jpg",
                'price': 0.0
            }),
            Product(**{
                'name': "Oversize Crates",
                'description': "Custom-built oversized crating solutions for large industrial equipment and machinery.",
                'category': "Specialty Solutions",
                'image_url': "/static/images/workshop.jpg",
                'price': 0.0
            })
        ]

        # Check and populate products independently
        if not Product.query.first():
            app.logger.info('Populating sample products data...')
            for product in sample_products:
                db.session.add(product)
            db.session.commit()
            products_count = Product.query.count()
            featured_products = Product.query.limit(3).all()
            app.logger.info(f'Added {products_count} products successfully. Featured products: {len(featured_products)}')

        # Check and populate testimonials independently
        if not Testimonial.query.first():
            app.logger.info('Populating sample testimonials data...')
            sample_testimonials = [
                Testimonial(**{
                    'client_name': "John D.",
                    'rating': 5,
                    'content': "Exceptional industrial packaging solutions! The custom crates perfectly protected our sensitive equipment during overseas shipping.",
                    'is_featured': True
                }),
                Testimonial(**{
                    'client_name': "Sarah M.",
                    'rating': 4,
                    'content': "Their ISPM 15 certified export crates ensured smooth customs clearance. Great attention to international shipping requirements.",
                    'is_featured': True
                }),
                Testimonial(**{
                    'client_name': "Michael R.",
                    'rating': 5,
                    'content': "The cushioned skids were perfect for our heavy machinery. Outstanding quality and professional service!",
                    'is_featured': True
                })
            ]
            for testimonial in sample_testimonials:
                db.session.add(testimonial)
            db.session.commit()
            testimonials_count = Testimonial.query.count()
            featured_testimonials = Testimonial.query.filter_by(is_featured=True).count()
            app.logger.info(f'Added {testimonials_count} testimonials successfully. Featured testimonials: {featured_testimonials}')

        # Check and populate gallery projects independently
        if not GalleryProject.query.first():
            app.logger.info('Populating sample gallery projects data...')
            sample_projects = [
        GalleryProject(
            title="Medical Equipment Export Package",
            description=
            "ISPM 15 certified export crates designed for sensitive medical equipment shipping to Europe. Features custom foam cushioning and moisture barriers.",
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
                "moisture_control":
                "Vapor barrier system",
                "cushioning":
                "Custom foam inserts",
                "monitoring":
                "Shock indicators installed"
            }),
            is_featured=True),
        GalleryProject(
            title="Industrial Press Shipping Solution",
            description=
            "Cushioned skids with integrated ramp system for 20-ton industrial equipment. Custom-engineered for repeated use and easy forklift access.",
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
            is_featured=True),
        GalleryProject(
            title="Wind Turbine Component Package",
            description=
            "Custom oversized crates for wind turbine components with specialized bracing and moisture control systems.",
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
            is_featured=True),
        GalleryProject(
            title="Electronics Reusable Export System",
            description=
            "Developed a reusable crating system with Skidmates for regular international shipments, reducing packaging waste by 85%.",
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
            is_featured=True)
    ]

    # Add the sample projects
            for project in sample_projects:
                db.session.add(project)
            db.session.commit()
            app.logger.info(f'Added {len(sample_projects)} gallery projects successfully')

        # Check and populate team members independently
        if not TeamMember.query.first():
            app.logger.info('Populating sample team members data...')
            sample_team = [
                TeamMember(
                    name="John Smith",
                    role="CEO & Founder",
                    bio="30+ years of expertise in custom industrial packaging solutions and international shipping.",
                    order=1,
                    is_active=True),
                TeamMember(
                    name="Sarah Johnson",
                    role="Operations Director",
                    bio="25+ years of manufacturing and industrial packaging operations expertise.",
                    order=2,
                    is_active=True),
                TeamMember(
                    name="Michael Brown",
                    role="Engineering Manager",
                    bio="20+ years of custom wood crating and export packaging design experience.",
                    order=3,
                    is_active=True)
            ]
            for member in sample_team:
                db.session.add(member)
            db.session.commit()
            app.logger.info('Sample team members populated successfully')

except Exception as e:
    app.logger.error(f'Failed to initialize database: {str(e)}')
    raise
