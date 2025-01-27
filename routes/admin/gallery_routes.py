from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required
from models import GalleryProject
from app import db
from routes.utils.upload import handle_file_upload
from routes.utils.error_handlers import handle_exceptions, log_route_access
from datetime import date
import json

gallery_bp = Blueprint('admin_gallery_bp', __name__)

@gallery_bp.route('/')
@login_required
@log_route_access('admin_gallery')
def index():
    try:
        # Get existing categories and industries for the form
        categories = [(cat[0],) for cat in db.session.query(GalleryProject.category).distinct().order_by(GalleryProject.category).all() if cat[0]]
        industries = [(ind[0],) for ind in db.session.query(GalleryProject.industry_served).distinct().order_by(GalleryProject.industry_served).all() if ind[0]]
        
        current_app.logger.debug(f'Found {len(categories)} categories and {len(industries)} industries')
        
        # For GET requests, fetch all gallery projects
        projects = GalleryProject.query.order_by(GalleryProject.completion_date.desc()).all()
        return render_template('admin/gallery.html', 
                             projects=projects,
                             categories=categories,
                             industries=industries)
    except Exception as e:
        current_app.logger.error(f'Error in gallery index: {str(e)}')
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('admin.dashboard'))

@gallery_bp.route('/create', methods=['POST'])
@login_required
@log_route_access('create_gallery_project')
def create():
    try:
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        
        # Handle category (existing or new)
        new_category = request.form.get('new_category', '').strip()
        category = new_category if new_category else request.form.get('category', '').strip()
        
        # Handle industry (existing or new)
        new_industry = request.form.get('new_industry', '').strip()
        industry_served = new_industry if new_industry else request.form.get('industry_served', '').strip()
        
        size_category = request.form.get('size_category', '').strip()
        weight_capacity = request.form.get('weight_capacity', '').strip()
        client = request.form.get('client', '').strip()
        completion_time = request.form.get('completion_time')
        ispm_compliant = bool(request.form.get('ispm_compliant', False))
        is_featured = bool(request.form.get('is_featured', False))
        
        # Validate required fields
        if not all([title, description, category, industry_served, size_category]):
            flash('All required fields must be filled', 'error')
            return redirect(url_for('admin.admin_gallery_bp.index'))
        
        # Handle image upload
        image = request.files.get('image')
        image_path = "/static/images/workshop.jpg"  # Default image
        
        if image and image.filename:
            try:
                upload_result = handle_file_upload(image)
                # Handle both dictionary and string return values
                if isinstance(upload_result, dict):
                    image_path = upload_result['original']
                else:
                    image_path = upload_result
            except ValueError as e:
                flash(str(e), 'error')
                return redirect(url_for('admin.admin_gallery_bp.index'))
            except Exception as e:
                flash(f'Error saving image: {str(e)}', 'error')
                return redirect(url_for('admin.admin_gallery_bp.index'))

        # Create new gallery project
        project = GalleryProject()
        project.title = title
        project.description = description
        project.image_url = image_path
        project.category = category
        project.industry_served = industry_served
        project.size_category = size_category
        project.weight_capacity = weight_capacity
        project.client = client
        project.completion_time = completion_time
        project.ispm_compliant = ispm_compliant
        project.is_featured = is_featured
        project.completion_date = date.today()
        
        # Handle special features
        special_features = {}
        feature_types = request.form.getlist('feature_type[]')
        custom_feature_types = request.form.getlist('custom_feature_type[]')
        feature_descriptions = request.form.getlist('feature_description[]')
        
        # Combine feature types and descriptions
        for i in range(len(feature_types)):
            if feature_types[i] and feature_descriptions[i]:
                # Use custom feature type if selected
                feature_type = custom_feature_types[i] if feature_types[i] == 'custom' and custom_feature_types[i] else feature_types[i]
                if feature_type:  # Only add if we have a valid feature type
                    special_features[feature_type] = feature_descriptions[i]
        
        project.special_features = json.dumps(special_features)
        
        try:
            db.session.add(project)
            db.session.commit()
            flash('Gallery project added successfully', 'success')
            return redirect(url_for('admin.admin_gallery_bp.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding gallery project: {str(e)}', 'error')
        
        return redirect(url_for('admin.admin_gallery_bp.index'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('admin.admin_gallery_bp.index'))

@gallery_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@log_route_access('edit_gallery_project')
def edit(id):
    try:
        project = GalleryProject.query.get_or_404(id)
        current_app.logger.debug(f'Found project: {project.title}')
        
        # Get existing categories and industries for the form
        try:
            categories = [(cat[0],) for cat in db.session.query(GalleryProject.category).distinct().order_by(GalleryProject.category).all() if cat[0]]
            industries = [(ind[0],) for ind in db.session.query(GalleryProject.industry_served).distinct().order_by(GalleryProject.industry_served).all() if ind[0]]
            current_app.logger.debug(f'Found {len(categories)} categories and {len(industries)} industries')
        except Exception as e:
            current_app.logger.error(f'Error fetching categories/industries: {str(e)}')
            flash(f'Error fetching categories: {str(e)}', 'error')
            return render_template('admin/edit_project.html', 
                                project=project,
                                categories=[],
                                industries=[])
        
        if request.method == 'POST':
            try:
                project.title = request.form.get('title')
                project.description = request.form.get('description')
                
                # Handle category (existing or new)
                new_category = request.form.get('new_category', '').strip()
                project.category = new_category if new_category else request.form.get('category', '').strip()
                
                # Handle industry (existing or new)
                new_industry = request.form.get('new_industry', '').strip()
                project.industry_served = new_industry if new_industry else request.form.get('industry_served', '').strip()
                
                project.size_category = request.form.get('size_category')
                project.weight_capacity = request.form.get('weight_capacity')
                project.client = request.form.get('client')
                project.completion_time = request.form.get('completion_time')
                project.ispm_compliant = bool(request.form.get('ispm_compliant'))
                project.is_featured = bool(request.form.get('is_featured'))
                
                current_app.logger.debug('Updated basic project fields')

                # Handle image upload
                image = request.files.get('image')
                if image and image.filename:
                    try:
                        upload_result = handle_file_upload(image)
                        if isinstance(upload_result, dict):
                            project.image_url = upload_result['original']
                        else:
                            project.image_url = upload_result
                        current_app.logger.debug(f'Updated image: {project.image_url}')
                    except Exception as e:
                        current_app.logger.error(f'Error uploading image: {str(e)}')
                        flash(f'Error saving image: {str(e)}', 'error')
                        return redirect(url_for('admin.admin_gallery_bp.index'))

                # Handle special features
                try:
                    special_features = {}
                    feature_types = request.form.getlist('feature_type[]')
                    custom_feature_types = request.form.getlist('custom_feature_type[]')
                    feature_descriptions = request.form.getlist('feature_description[]')
                    
                    for i in range(len(feature_types)):
                        if feature_types[i] and feature_descriptions[i]:
                            feature_type = custom_feature_types[i] if feature_types[i] == 'custom' and custom_feature_types[i] else feature_types[i]
                            if feature_type:
                                special_features[feature_type] = feature_descriptions[i]
                    
                    project.special_features = json.dumps(special_features)
                    current_app.logger.debug(f'Updated special features: {special_features}')
                except Exception as e:
                    current_app.logger.error(f'Error processing special features: {str(e)}')
                    raise

                try:
                    db.session.commit()
                    flash('Project updated successfully', 'success')
                    current_app.logger.info(f'Successfully updated project {project.id}')
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.error(f'Database error updating project: {str(e)}')
                    flash(f'Error updating project: {str(e)}', 'error')
                return redirect(url_for('admin.admin_gallery_bp.index'))

            except Exception as e:
                current_app.logger.error(f'Error in POST processing: {str(e)}')
                flash(f'Error updating project: {str(e)}', 'error')
                return render_template('admin/edit_project.html', 
                                    project=project,
                                    categories=categories,
                                    industries=industries)

        # For GET requests
        try:
            if project.special_features:
                try:
                    project.special_features = json.loads(project.special_features)
                except (json.JSONDecodeError, Exception) as e:
                    current_app.logger.error(f'Error parsing special features: {str(e)}')
                    project.special_features = {}
            else:
                project.special_features = {}
            
            return render_template('admin/edit_project.html', 
                                project=project,
                                categories=categories,
                                industries=industries)
        except Exception as e:
            current_app.logger.error(f'Error preparing GET response: {str(e)}')
            flash(f'Error loading project: {str(e)}', 'error')
            return render_template('admin/edit_project.html', 
                                project=project,
                                categories=categories,
                                industries=industries)

    except Exception as e:
        current_app.logger.error(f'Unhandled error in edit route: {str(e)}')
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('admin.admin_gallery_bp.index'))

@gallery_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@log_route_access('delete_gallery_project')
def delete(id):
    try:
        project = GalleryProject.query.get_or_404(id)
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting project: {str(e)}', 'error')
    return redirect(url_for('admin.admin_gallery_bp.index'))
