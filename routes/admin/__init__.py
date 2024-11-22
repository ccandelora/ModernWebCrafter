from flask import Blueprint
from routes.admin.routes import admin
from routes.admin.product_routes import products_bp
from routes.admin.gallery_routes import gallery_bp
from routes.admin.testimonial_routes import testimonials_bp
from routes.admin.team_routes import team_bp

# Register blueprints with URL prefixes
admin.register_blueprint(products_bp, url_prefix='/products')
admin.register_blueprint(gallery_bp, url_prefix='/gallery')
admin.register_blueprint(testimonials_bp, url_prefix='/testimonials')
admin.register_blueprint(team_bp, url_prefix='/team')
