from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required
from models import Product
from app import db
from routes.utils.upload import handle_file_upload
from routes.utils.validation import validate_product_data
from routes.utils.error_handlers import handle_exceptions, log_route_access

products_bp = Blueprint('admin_products', __name__)

@products_bp.route('/', methods=['GET', 'POST'])
@login_required
@log_route_access('admin_products')
@handle_exceptions
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
                    image_paths = handle_file_upload(image)
                    image_path = image_paths['original']  # Use the original image URL
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
            product.image_url = image_path  # Store only the original image URL

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

@products_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@log_route_access('edit_product')
@handle_exceptions
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.category = request.form.get('category')
        product.description = request.form.get('description')

        image = request.files.get('image')
        if image and image.filename:
            try:
                new_image_paths = handle_file_upload(image, old_file_path=product.image_url)
                product.image_url = new_image_paths['original']  # Use the original image URL
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

@products_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@log_route_access('delete_product')
@handle_exceptions
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully', 'success')
    return redirect(url_for('admin.products'))
