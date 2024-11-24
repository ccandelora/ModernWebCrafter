from app import db, app
from models import Product, Testimonial, GalleryProject, TeamMember
from datetime import date
import json
import logging

logger = logging.getLogger(__name__)

def init_sample_data():
    """Initialize sample data only if tables are empty."""
    try:
        with app.app_context():
            # Only add sample data if tables are empty
            if not Product.query.first():
                logger.info("Initializing sample products...")
                sample_products = [
                    Product(
                        name="ISPM 15 Certified Export Crates",
                        description="International shipping standard compliant crates for export. Features heat treatment certification and proper IPPC marking.",
                        category="Export Crates",
                        image_url="/static/images/workshop.jpg",
                        price=0.0
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
                for product in sample_products:
                    db.session.add(product)

            if not Testimonial.query.first():
                logger.info("Initializing sample testimonials...")
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

            if not GalleryProject.query.first():
                logger.info("Initializing sample gallery projects...")
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
                    )
                ]
                for project in sample_projects:
                    db.session.add(project)

            if not TeamMember.query.first():
                logger.info("Initializing sample team members...")
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

            db.session.commit()
            logger.info("Sample data initialization completed successfully")
    except Exception as e:
        logger.error(f"Error initializing sample data: {str(e)}")
        db.session.rollback()
        raise

if __name__ == "__main__":
    init_sample_data()
