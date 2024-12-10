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
                return redirect(url_for('admin.admin_products.products'))

            image = request.files.get('image')
            image_path = "/static/images/workshop.jpg"  # Default image

            if image and image.filename:
                try:
                    image_paths = handle_file_upload(image)
                    image_path = image_paths['original']  # Use the original image URL
                except ValueError as e:
                    flash(str(e), 'error')
                    return redirect(url_for('admin.admin_products.products'))
                except Exception as e:
                    flash(f'Error saving image: {str(e)}', 'error')
                    return redirect(url_for('admin.admin_products.products'))

            product = Product()
            product.name = name
            product.category = category
            product.description = description
            product.image_url = image_path
            product.is_featured = bool(request.form.get('is_featured'))

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

            return redirect(url_for('admin.admin_products.products'))

        # GET request handling
        current_app.logger.debug('Fetching all products from database')
        products = Product.query.all()
        current_app.logger.debug(f'Found {len(products)} products')
        
        try:
            # Organize products by category
            categorized_products = {}
            uncategorized_products = []
            
            # First pass: collect categories
            categories = set()
            for product in products:
                if product.category and product.category.strip():
                    categories.add(product.category.strip())
            sorted_categories = sorted(categories)
            
            # Second pass: organize products
            for product in products:
                if product.category and product.category.strip():
                    category = product.category.strip()
                    if category not in categorized_products:
                        categorized_products[category] = []
                    categorized_products[category].append(product)
                else:
                    uncategorized_products.append(product)
            
            current_app.logger.debug(f'Successfully categorized {len(products)} products into {len(sorted_categories)} categories')
            
            return render_template('admin/products.html', 
                                products=products,
                                sorted_categories=sorted_categories,
                                categorized_products=categorized_products,
                                uncategorized_products=uncategorized_products)
                                
        except Exception as category_error:
            current_app.logger.error(f'Error categorizing products: {str(category_error)}')
            # Fall back to uncategorized view if categorization fails
            return render_template('admin/products.html', 
                                products=products,
                                sorted_categories=[],
                                categorized_products={},
                                uncategorized_products=products)
            
    except Exception as e:
        current_app.logger.error(f'Error in admin products route: {str(e)}')
        current_app.logger.exception('Full traceback:')
        flash('Error loading products. Please try again later.', 'error')
        return render_template('errors/500.html'), 500

@products_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@log_route_access('edit_product')
@handle_exceptions
def edit_product(id):
    try:
        product = Product.query.get_or_404(id)
        if request.method == 'POST':
            product.name = request.form.get('name')
            product.category = request.form.get('category')
            product.description = request.form.get('description')
            product.is_featured = bool(request.form.get('is_featured'))

            image = request.files.get('image')
            if image and image.filename:
                try:
                    new_image_paths = handle_file_upload(image, old_file_path=product.image_url)
                    product.image_url = new_image_paths['original']  # Use the original image URL
                except ValueError as e:
                    flash(str(e), 'error')
                    return redirect(url_for('admin.admin_products.products'))
                except Exception as e:
                    flash(f'Error saving image: {str(e)}', 'error')
                    return redirect(url_for('admin.admin_products.products'))

            db.session.commit()
            flash('Product updated successfully', 'success')
            return redirect(url_for('admin.admin_products.products'))

        return render_template('admin/edit_product.html', product=product)
    except Exception as e:
        current_app.logger.error(f'Error editing product {id}: {str(e)}')
        current_app.logger.exception('Full traceback:')
        flash('Error editing product. Please try again later.', 'error')
        return redirect(url_for('admin.admin_products.products'))

@products_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@log_route_access('delete_product')
@handle_exceptions
def delete_product(id):
    try:
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully', 'success')
    except Exception as e:
        current_app.logger.error(f'Error deleting product {id}: {str(e)}')
        current_app.logger.exception('Full traceback:')
        flash('Error deleting product. Please try again later.', 'error')
        db.session.rollback()
    return redirect(url_for('admin.admin_products.products'))
