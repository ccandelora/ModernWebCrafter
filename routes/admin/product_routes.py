from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from models import Product
from app import db
from routes.utils.upload import handle_file_upload
from routes.utils.error_handlers import handle_exceptions, log_route_access

products_bp = Blueprint('admin_products', __name__)

@products_bp.route('/')
@login_required
@log_route_access('admin_products')
@handle_exceptions
def products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@products_bp.route('/add', methods=['POST'])
@login_required
@log_route_access('add_product')
@handle_exceptions
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        description = request.form.get('description')
        
        product = Product(
            name=name,
            category=category,
            description=description
        )
        
        image = request.files.get('image')
        if image:
            try:
                image_path = handle_file_upload(image)
                product.image_url = image_path
            except Exception as e:
                flash(f'Error uploading image: {str(e)}', 'error')
                return redirect(url_for('admin_products.products'))
        
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully', 'success')
        
    return redirect(url_for('admin_products.products'))

@products_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
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
        if image:
            try:
                image_path = handle_file_upload(image)
                product.image_url = image_path
            except Exception as e:
                flash(f'Error uploading image: {str(e)}', 'error')
                return render_template('admin/edit_product.html', product=product)
        
        db.session.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('admin_products.products'))
    
    return render_template('admin/edit_product.html', product=product)

@products_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@log_route_access('delete_product')
@handle_exceptions
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully', 'success')
    return redirect(url_for('admin_products.products'))
