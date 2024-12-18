from flask import Blueprint
from routes.admin.routes import admin
from routes.admin.product_routes import products_bp
from routes.admin.gallery_routes import gallery_bp
from routes.admin.testimonial_routes import testimonials_bp
from routes.admin.team_routes import team_bp

# Export the admin blueprint
__all__ = ['admin']

# Register blueprints with URL prefixes
# These registrations are done in routes.py instead of here
# to avoid duplicate registrations
