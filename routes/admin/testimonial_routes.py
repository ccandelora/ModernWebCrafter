from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from models import Testimonial
from app import db
from routes.utils.error_handlers import handle_exceptions, log_route_access

testimonials_bp = Blueprint('admin_testimonials', __name__)

@testimonials_bp.route('/', methods=['GET', 'POST'])
@login_required
@log_route_access('admin_testimonials')
@handle_exceptions
def testimonials():
    """Handle testimonials management."""
    if request.method == 'POST':
        testimonial = Testimonial()
        testimonial.client_name = request.form['client_name']
        testimonial.rating = int(request.form['rating'])
        testimonial.content = request.form['content']
        testimonial.is_featured = bool(request.form.get('is_featured', False))
        db.session.add(testimonial)
        db.session.commit()
        flash('Testimonial added successfully!', 'success')
        return redirect(url_for('admin.testimonials'))

    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('admin/testimonials.html', testimonials=testimonials)
