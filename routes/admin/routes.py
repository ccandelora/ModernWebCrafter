from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from models import Product, GalleryProject, Testimonial
from app import db
from routes.utils.upload import handle_file_upload
from datetime import date
import json

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    try:
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            category = request.form.get('category', '').strip()
            description = request.form.get('description', '').strip()

            if not all([name, category, description]):
                flash('All fields are required', 'error')
                return redirect(url_for('admin.products'))

            image = request.files.get('image')
            image_path = "/static/images/workshop.jpg"  # Default image

            if image and image.filename:
                try:
                    image_path = handle_file_upload(image)
                except ValueError as e:
                    flash(str(e), 'error')
                    return redirect(url_for('admin.products'))
                except Exception as e:
                    flash(f'Error saving image: {str(e)}', 'error')
                    return redirect(url_for('admin.products'))

            product = Product()
            product.name = name
            product.category = category
            product.description = description
            product.image_url = image_path

            try:
                # Handle price field
                price = float(request.form.get('price', 0.0))
                product.price = price

                db.session.add(product)
                db.session.commit()
                flash('Product added successfully', 'success')
            except ValueError:
                db.session.rollback()
                flash('Invalid price value', 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding product: {str(e)}', 'error')

            return redirect(url_for('admin.products'))

        products = Product.query.all()
        return render_template('admin/products.html', products=products)
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('admin.dashboard'))

@admin.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.category = request.form.get('category')
        product.description = request.form.get('description')

        image = request.files.get('image')
        if image and image.filename:
            try:
                new_image_path = handle_file_upload(image, old_file_path=product.image_url)
                product.image_url = new_image_path
            except ValueError as e:
                flash(str(e), 'error')
                return redirect(url_for('admin.products'))
            except Exception as e:
                flash(f'Error saving image: {str(e)}', 'error')
                return redirect(url_for('admin.products'))

        db.session.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/edit_product.html', product=product)

@admin.route('/products/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully', 'success')
    return redirect(url_for('admin.products'))

@admin.route('/testimonials', methods=['GET', 'POST'])
@login_required
def testimonials():
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

@admin.route('/gallery', methods=['GET', 'POST'])
@login_required
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
