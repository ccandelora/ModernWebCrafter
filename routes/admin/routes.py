from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from models import Product, GalleryProject, Testimonial, Admin, TeamMember
from app import db
from routes.utils.error_handlers import handle_exceptions, log_route_access
from routes.admin.product_routes import products_bp
from routes.admin.gallery_routes import gallery_bp
from routes.admin.testimonial_routes import testimonials_bp
from routes.admin.team_routes import team_bp

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.before_request
def verify_admin():
    """Verify admin authentication."""
    if not current_user.is_authenticated:
        current_app.logger.warning(f'Unauthorized dashboard access attempt from {request.remote_addr}')
        flash('Please log in to access the admin dashboard', 'error')
        return redirect(url_for('auth.login'))

@admin.before_request
def verify_db():
    """Verify database connection."""
    try:
        db.session.query(Admin).first()
    except Exception as e:
        current_app.logger.error(f'Database connection error: {str(e)}')
        return render_template('errors/500.html'), 500

@admin.before_request
def log_request_info():
    """Log detailed information about each request to admin routes."""
    current_app.logger.debug(
        'Admin Route Request:\n'
        f'Path: {request.path}\n'
        f'Method: {request.method}\n'
        f'User: {current_user.username if not current_user.is_anonymous else "anonymous"}\n'
        f'IP: {request.remote_addr}\n'
        f'User Agent: {request.user_agent.string}'
    )

@admin.route('/')
@login_required
@log_route_access('admin_dashboard')
@handle_exceptions
def dashboard():
    """Render the admin dashboard with enhanced logging and error handling."""
    current_app.logger.debug(f'Dashboard access attempt by user: {current_user.username}')
    try:
        stats = {
            'products': Product.query.count(),
            'gallery_projects': GalleryProject.query.count(),
            'testimonials': Testimonial.query.count()
        }
        current_app.logger.debug(f'Dashboard stats retrieved: {stats}')
        return render_template('admin/dashboard.html', stats=stats)
    except Exception as e:
        current_app.logger.error(f'Dashboard error: {str(e)}')
        return render_template('errors/500.html'), 500
@admin.route('/products')
@login_required
@log_route_access('admin_products')
@handle_exceptions
def products():
    return products_bp.products()

@admin.route('/gallery')
@login_required
@log_route_access('admin_gallery')
@handle_exceptions
def gallery():
    return gallery_bp.gallery()

@admin.route('/testimonials')
@login_required
@log_route_access('admin_testimonials')
@handle_exceptions
def testimonials():
    return testimonials_bp.testimonials()

@admin.route('/team')
@login_required
@log_route_access('admin_team')
@handle_exceptions
def team():
    team_members = TeamMember.query.order_by(TeamMember.order.asc()).all()
    return render_template('admin/team.html', team_members=team_members)