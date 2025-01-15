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
        return redirect(url_for('admin.admin_testimonials_bp.testimonials'))

    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('admin/testimonials.html', testimonials=testimonials)

@testimonials_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@log_route_access('edit_testimonial')
@handle_exceptions
def edit_testimonial(id):
    """Handle editing a testimonial."""
    testimonial = Testimonial.query.get_or_404(id)
    
    if request.method == 'POST':
        testimonial.client_name = request.form['client_name']
        testimonial.rating = int(request.form['rating'])
        testimonial.content = request.form['content']
        testimonial.is_featured = bool(request.form.get('is_featured', False))
        
        try:
            db.session.commit()
            flash('Testimonial updated successfully!', 'success')
            return redirect(url_for('admin.admin_testimonials_bp.testimonials'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating testimonial. Please try again.', 'error')
            return redirect(url_for('admin.admin_testimonials_bp.testimonials'))
    
    return render_template('admin/edit_testimonial.html', testimonial=testimonial)

@testimonials_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@log_route_access('delete_testimonial')
@handle_exceptions
def delete_testimonial(id):
    """Handle deleting a testimonial."""
    testimonial = Testimonial.query.get_or_404(id)
    try:
        db.session.delete(testimonial)
        db.session.commit()
        flash('Testimonial deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting testimonial. Please try again.', 'error')
    
    return redirect(url_for('admin.admin_testimonials_bp.testimonials'))
