from flask import Blueprint
from routes.admin.routes import admin
from routes.admin.product_routes import products_bp
from routes.admin.gallery_routes import gallery_bp
from routes.admin.testimonial_routes import testimonials_bp
from routes.admin.team_routes import team_bp

# Initialize the main admin blueprint
admin.register_blueprint(products_bp)
admin.register_blueprint(gallery_bp)
admin.register_blueprint(testimonials_bp)
admin.register_blueprint(team_bp)
