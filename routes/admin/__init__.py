from flask import Blueprint
from routes.admin.routes import admin
from routes.admin.product_routes import products_bp
from routes.admin.gallery_routes import gallery_bp
from routes.admin.testimonial_routes import testimonials_bp
from routes.admin.team_routes import team_bp

# Initialize blueprints with URL prefixes
products_bp = Blueprint('admin_products', __name__, url_prefix='/products')
gallery_bp = Blueprint('admin_gallery', __name__, url_prefix='/gallery')
testimonials_bp = Blueprint('admin_testimonials', __name__, url_prefix='/testimonials')
team_bp = Blueprint('admin_team', __name__, url_prefix='/team')

# Register blueprints with the main admin blueprint
admin.register_blueprint(products_bp)
admin.register_blueprint(gallery_bp)
admin.register_blueprint(testimonials_bp)
admin.register_blueprint(team_bp)
