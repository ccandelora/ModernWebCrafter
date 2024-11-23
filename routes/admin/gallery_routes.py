from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from models import GalleryProject
from app import db
from routes.utils.upload import handle_file_upload
from routes.utils.error_handlers import handle_exceptions, log_route_access
from datetime import date
import json

gallery_bp = Blueprint('admin_gallery', __name__)

@gallery_bp.route('/', methods=['GET', 'POST'])
@login_required
@log_route_access('admin_gallery')
@handle_exceptions
def gallery():
    try:
        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            category = request.form.get('category', '').strip()
            industry_served = request.form.get('industry_served', '').strip()
            size_category = request.form.get('size_category', '').strip()
            weight_capacity = request.form.get('weight_capacity', '').strip()
            ispm_compliant = bool(request.form.get('ispm_compliant', False))
            is_featured = bool(request.form.get('is_featured', False))
            
            # Validate required fields
            if not all([title, description, category, industry_served, size_category]):
                flash('All required fields must be filled', 'error')
                return redirect(url_for('admin.gallery'))
            
            # Handle image upload
            image = request.files.get('image')
            image_path = "/static/images/workshop.jpg"  # Default image
            
            if image and image.filename:
                try:
                    image_path = handle_file_upload(image)
                except ValueError as e:
                    flash(str(e), 'error')
                    return redirect(url_for('admin.gallery'))
                except Exception as e:
                    flash(f'Error saving image: {str(e)}', 'error')
                    return redirect(url_for('admin.gallery'))
            
            # Create new gallery project
            project = GalleryProject()
            project.title = title
            project.description = description
            project.image_url = image_path
            project.category = category
            project.industry_served = industry_served
            project.size_category = size_category
            project.weight_capacity = weight_capacity
            project.ispm_compliant = ispm_compliant
            project.is_featured = is_featured
            project.completion_date = date.today()
            
            # Handle special features as JSON
            special_features = {}
            for feature in ['moisture_control', 'cushioning', 'monitoring', 'bracing', 'reusability', 'security']:
                if request.form.get(f'feature_{feature}'):
                    special_features[feature] = request.form.get(f'feature_description_{feature}', '')
            project.special_features = json.dumps(special_features)
            
            try:
                db.session.add(project)
                db.session.commit()
                flash('Gallery project added successfully', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding gallery project: {str(e)}', 'error')
            
            return redirect(url_for('admin.gallery'))
        
        # For GET requests, fetch all gallery projects
        projects = GalleryProject.query.order_by(GalleryProject.completion_date.desc()).all()
        return render_template('admin/gallery.html', projects=projects)
        
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('admin.dashboard'))

@gallery_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@log_route_access('edit_gallery_project')
@handle_exceptions
def edit_gallery_project(id):
    project = GalleryProject.query.get_or_404(id)
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.category = request.form.get('category')
        project.industry_served = request.form.get('industry_served')
        project.size_category = request.form.get('size_category')
        project.weight_capacity = request.form.get('weight_capacity')
        project.ispm_compliant = bool(request.form.get('ispm_compliant'))
        project.is_featured = bool(request.form.get('is_featured'))

        image = request.files.get('image')
        if image and image.filename:
            try:
                new_image_path = handle_file_upload(image, old_file_path=project.image_url)
                project.image_url = new_image_path
            except Exception as e:
                flash(str(e), 'error')
                return redirect(url_for('admin.admin_gallery.gallery'))

        db.session.commit()
        flash('Project updated successfully', 'success')
        return redirect(url_for('admin.admin_gallery.gallery'))

    return render_template('admin/edit_project.html', project=project)

@gallery_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@log_route_access('delete_gallery_project')
@handle_exceptions
def delete_project(id):
    project = GalleryProject.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully', 'success')
    return redirect(url_for('admin.admin_gallery.gallery'))
