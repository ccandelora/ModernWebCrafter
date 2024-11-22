import os
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_dir():
    upload_dir = os.path.join('static', 'images', 'uploads')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return upload_dir

def handle_file_upload(file, old_file_path=None):
    if not allowed_file(file.filename):
        raise ValueError('Invalid file format. Please use PNG, JPG, JPEG or GIF')
    
    upload_dir = ensure_upload_dir()
    secure_name = secure_filename(file.filename)
    file_path = f"/static/images/uploads/{secure_name}"
    full_path = os.path.join('.', file_path)
    
    # Save the new file
    file.save(full_path)
    if not os.path.exists(full_path):
        raise ValueError("Failed to save the file")
    
    # If there was an old file and it's not the default image, try to remove it
    if old_file_path and 'avatar-placeholder.svg' not in old_file_path:
        try:
            old_full_path = os.path.join('.', old_file_path)
            if os.path.exists(old_full_path):
                os.remove(old_full_path)
        except Exception:
            pass  # Ignore errors when trying to remove old file
    
    return file_path
# Create uploads directory if it doesn't exist
if not os.path.exists('./static/images/uploads'):
    os.makedirs('./static/images/uploads', exist_ok=True)

import json
from datetime import date
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from models import Product, GalleryProject, Testimonial, Admin, Inquiry, TeamMember

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    if not filename:
        return False
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Helper function to create upload directory
def ensure_upload_dir():
    upload_dir = './static/images/uploads'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return upload_dir


# Helper function to handle file uploads
def handle_file_upload(file, current_path="/static/images/uploads"):
    if not file or not file.filename:
        return current_path

    if not allowed_file(file.filename):
        raise ValueError(
            'Invalid file format. Please use PNG, JPG, JPEG or GIF')

    # Ensure upload directory exists
    upload_dir = './static/images/uploads'
    os.makedirs(upload_dir, exist_ok=True)

    secure_name = secure_filename(file.filename)
    image_path = f"/static/images/uploads/{secure_name}"

    try:
        file.save(os.path.join('.', image_path))
        return image_path
    except Exception as e:
        raise ValueError(f'Error saving file: {str(e)}')


@app.route('/')
def index():
    featured_products = Product.query.limit(3).all()
    testimonials = Testimonial.query.filter_by(is_featured=True).limit(3).all()
    return render_template('index.html',
                           products=featured_products,
                           testimonials=testimonials)


@app.route('/about')
def about():
    team_members = TeamMember.query.filter_by(is_active=True).order_by(
        TeamMember.order.asc()).all()
    return render_template('about.html', team_members=team_members)


@app.route('/products')
def products():
    category = request.args.get('category')
    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    categories = db.session.query(Product.category).distinct()
    return render_template('products.html',
                           products=products,
                           categories=categories)


@app.route('/quote', methods=['GET', 'POST'])
def quote_calculator():
    if request.method == 'POST':
        # Get form data
        package_type = request.form.get('package_type')
        length = float(request.form.get('length', 0))
        width = float(request.form.get('width', 0))
        height = float(request.form.get('height', 0))
        weight = float(request.form.get('weight', 0))
        requirements = request.form.getlist('requirements[]')
        shipping_type = request.form.get('shipping_type')

        # Calculate cubic feet
        cubic_feet = (length * width *
                      height) / 1728  # Convert cubic inches to cubic feet

        # Base rates per cubic foot for different package types
        base_rates = {
            'export_crate': 12.0,
            'cushioned_crate': 15.0,
            'skidmate': 10.0,
            'cushion_skid': 14.0,
            'oversize': 18.0
        }

        # Calculate base cost
        base_cost = cubic_feet * base_rates.get(package_type, 12.0)

        # Add weight factor
        weight_factor = max(1.0,
                            weight / 1000)  # Increase cost for heavy items
        base_cost *= weight_factor

        # Add costs for special requirements
        requirement_costs = {
            'moisture_barrier': 200,
            'shock_absorption': 300,
            'custom_foam': 400,
            'ramp_system': 500
        }

        for req in requirements:
            base_cost += requirement_costs.get(req, 0)

        # International shipping markup
        if shipping_type == 'international':
            base_cost *= 1.3  # 30% markup for international

        # Add range for estimate
        min_cost = round(base_cost * 0.9, 2)
        max_cost = round(base_cost * 1.1, 2)

        estimated_quote = {'min': min_cost, 'max': max_cost}

        return render_template('quote.html', estimated_quote=estimated_quote)

    return render_template('quote.html')


@app.route('/gallery')
def gallery():
    category = request.args.get('category')
    industry = request.args.get('industry')
    size = request.args.get('size')

    query = GalleryProject.query

    if category:
        query = query.filter_by(category=category)
    if industry:
        query = query.filter_by(industry_served=industry)
    if size:
        query = query.filter_by(size_category=size)

    projects = query.order_by(GalleryProject.completion_date.desc()).all()

    categories = db.session.query(GalleryProject.category).distinct()
    industries = db.session.query(GalleryProject.industry_served).distinct()
    sizes = db.session.query(GalleryProject.size_category).distinct()

    return render_template('gallery.html',
                           projects=projects,
                           categories=categories,
                           industries=industries,
                           sizes=sizes,
                           selected_category=category,
                           selected_industry=industry,
                           selected_size=size)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Create new inquiry with additional fields
        inquiry = Inquiry(name=request.form['name'],
                          email=request.form['email'],
                          company=request.form.get('company', ''),
                          industry=request.form.get('industry', ''),
                          package_type=request.form.get('package_type', ''),
                          message=request.form['message'])
        if 'product_id' in request.form:
            inquiry.product_id = request.form['product_id']

        db.session.add(inquiry)
        db.session.commit()
        flash(
            'Thank you for your inquiry! Our team will contact you within 1 business day.',
            'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')


@app.route('/admin/testimonials', methods=['GET', 'POST'])
@login_required
def manage_testimonials():
    if request.method == 'POST':
        testimonial = Testimonial(client_name=request.form['client_name'],
                                  rating=int(request.form['rating']),
                                  content=request.form['content'],
                                  is_featured=bool(
                                      request.form.get('is_featured', False)))
        db.session.add(testimonial)
        db.session.commit()
        flash('Testimonial added successfully!', 'success')
        return redirect(url_for('manage_testimonials'))

    testimonials = Testimonial.query.order_by(
        Testimonial.created_at.desc()).all()
    return render_template('admin/testimonials.html',
                           testimonials=testimonials)


@app.template_filter('parse_json')
def parse_json_filter(value):
    try:
        return json.loads(value)
    except:
        return {}


@app.context_processor
def utility_processor():

    def get_categories():
        return db.session.query(Product.category).distinct()

    return dict(get_categories=get_categories)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('admin/login.html')


@app.route('/admin/logout', methods=['POST'])
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))


@app.route('/admin')
@login_required
def admin_dashboard():
    return render_template('admin/dashboard.html')


@app.route('/admin/products', methods=['GET', 'POST'])
@login_required
def admin_products():
    try:
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            category = request.form.get('category', '').strip()
            description = request.form.get('description', '').strip()

            if not all([name, category, description]):
                flash('All fields are required', 'error')
                return redirect(url_for('admin_products'))

            image = request.files.get('image')
            image_path = "/static/images/workshop.jpg"

            if image and image.filename:
                if image.filename.lower().endswith(
                    ('.png', '.jpg', '.jpeg', '.gif')):
                    secure_name = secure_filename(image.filename)
                    image_path = f"/static/images/uploads/{secure_name}"
                    try:
                        os.makedirs('./static/images/uploads', exist_ok=True)
                        image.save('.' + image_path)
                    except Exception as e:
                        flash(f'Error saving image: {str(e)}', 'error')
                        return redirect(url_for('admin_products'))
                else:
                    flash(
                        'Invalid image format. Please use PNG, JPG, JPEG or GIF',
                        'error')
                    return redirect(url_for('admin_products'))

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

            return redirect(url_for('admin_products'))

        products = Product.query.all()
        return render_template('admin/products.html', products=products)
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))


@app.route('/admin/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.category = request.form.get('category')
        product.description = request.form.get('description')

        image = request.files.get('image')
        if image:
            image_path = f"/static/images/uploads/{secure_filename(image.filename)}"
            image.save('.' + image_path)
            product.image_url = image_path

        db.session.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('admin_products'))

    return render_template('admin/edit_product.html', product=product)


@app.route('/admin/products/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully', 'success')
    return redirect(url_for('admin_products'))


@app.route('/admin/gallery', methods=['GET', 'POST'])
@login_required
def admin_gallery():
    try:
        if request.method == 'POST':
            # Get and validate required fields
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            client = request.form.get('client', '').strip()
            category = request.form.get('category', '').strip()
            industry_served = request.form.get('industry_served', '').strip()
            size_category = request.form.get('size_category', '').strip()
            weight_capacity = request.form.get('weight_capacity', '').strip()

            # Validate required fields
            if not all([
                    title, description, client, category, industry_served,
                    size_category, weight_capacity
            ]):
                flash('All required fields must be filled out', 'error')
                return redirect(url_for('admin_gallery'))

            try:
                completion_time = int(request.form.get('completion_time', 0))
                if completion_time <= 0:
                    raise ValueError("Completion time must be positive")
            except ValueError as e:
                flash(f'Invalid completion time: {str(e)}', 'error')
                return redirect(url_for('admin_gallery'))

            ispm_compliant = bool(request.form.get('ispm_compliant'))
            is_featured = bool(request.form.get('is_featured'))
            image = request.files.get('image')

            # Handle image upload
            image_path = "/static/images/workshop.jpg"
            if image and image.filename:
                if image.filename.lower().endswith(
                    ('.png', '.jpg', '.jpeg', '.gif')):
                    secure_name = secure_filename(image.filename)
                    image_path = f"/static/images/uploads/{secure_name}"
                    try:
                        os.makedirs('./static/images/uploads', exist_ok=True)
                        image.save('.' + image_path)
                    except Exception as e:
                        flash(f'Error saving image: {str(e)}', 'error')
                        return redirect(url_for('admin_gallery'))
                else:
                    flash(
                        'Invalid image format. Please use PNG, JPG, JPEG or GIF',
                        'error')
                    return redirect(url_for('admin_gallery'))

            try:
                project = GalleryProject()
                project.title = title
                project.description = description
                project.client = client
                project.category = category
                project.industry_served = industry_served
                project.completion_time = completion_time
                project.size_category = size_category
                project.weight_capacity = weight_capacity
                project.ispm_compliant = ispm_compliant
                project.is_featured = is_featured
                project.image_url = image_path
                project.completion_date = date.today()

                db.session.add(project)
                db.session.commit()
                flash('Project added successfully', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding project: {str(e)}', 'error')

            return redirect(url_for('admin_gallery'))

        projects = GalleryProject.query.all()
        return render_template('admin/gallery.html', projects=projects)
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))


@app.route('/admin/gallery/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = GalleryProject.query.get_or_404(id)
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.client = request.form.get('client')
        project.category = request.form.get('category')
        project.industry_served = request.form.get('industry_served')
        project.completion_time = int(request.form.get('completion_time'))
        project.size_category = request.form.get('size_category')
        project.weight_capacity = request.form.get('weight_capacity')
        project.ispm_compliant = bool(request.form.get('ispm_compliant'))
        project.is_featured = bool(request.form.get('is_featured'))

        image = request.files.get('image')
        if image:
            try:
                image_path = handle_file_upload(image, project.image_url)
                project.image_url = image_path
            except ValueError as e:
                flash(str(e), 'error')
                return redirect(url_for('admin_gallery'))

        db.session.commit()
        flash('Project updated successfully', 'success')
        return redirect(url_for('admin_gallery'))

    return render_template('admin/edit_project.html', project=project)


@app.route('/admin/team', methods=['GET', 'POST'])
@login_required
def admin_team():
    if request.method == 'POST':
        try:
            # Get and validate form data
            name = request.form.get('name', '').strip()
            role = request.form.get('role', '').strip()
            bio = request.form.get('bio', '').strip()
            order = request.form.get('order', '0')
            is_active = request.form.get('is_active') is not None

            # Validate required fields
            if not all([name, role, bio]):
                flash('Name, role, and bio are required fields', 'error')
                return redirect(url_for('admin_team'))

            # Validate order is a valid integer
            try:
                order = int(order)
            except ValueError:
                flash('Order must be a valid number', 'error')
                return redirect(url_for('admin_team'))

            # Create new team member
            member = TeamMember()
            member.name = name
            member.role = role
            member.bio = bio
            member.order = order
            member.is_active = is_active
            member.image_url = '/static/images/avatar-placeholder.svg'  # Default image

            # Handle image upload if provided
            image = request.files.get('image')
            if image and image.filename:
                if not allowed_file(image.filename):
                    flash(
                        'Invalid file format. Please use PNG, JPG, JPEG or GIF',
                        'error')
                    return redirect(url_for('admin_team'))
                try:
                    member.image_url = handle_file_upload(image)
                except ValueError as e:
                    flash(str(e), 'error')
                    return redirect(url_for('admin_team'))

            # Save to database
            try:
                db.session.add(member)
                db.session.commit()
                flash('Team member added successfully', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding team member: {str(e)}', 'error')

            return redirect(url_for('admin_team'))

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('admin_team'))

    # GET request - display team members
    team_members = TeamMember.query.order_by(TeamMember.order.asc()).all()
    return render_template('admin/team.html', team_members=team_members)


@app.route('/admin/team/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_team_member(id):
    member = TeamMember.query.get_or_404(id)
    if request.method == 'POST':
        try:
            # Get and validate form data
            name = request.form.get('name', '').strip()
            role = request.form.get('role', '').strip()
            bio = request.form.get('bio', '').strip()
            order = request.form.get('order', '0')
            is_active = request.form.get('is_active') is not None

            # Validate required fields
            if not all([name, role, bio]):
                flash('Name, role, and bio are required fields', 'error')
                return redirect(url_for('edit_team_member', id=id))

            # Validate order is a valid integer
            try:
                order = int(order)
            except ValueError:
                flash('Order must be a valid number', 'error')
                return redirect(url_for('edit_team_member', id=id))

            # Update member data
            member.name = name
            member.role = role
            member.bio = bio
            member.order = order
            member.is_active = is_active

            # Handle image upload if provided
            image = request.files.get('image')
            if image and image.filename:
                if not allowed_file(image.filename):
                    flash(
                        'Invalid file format. Please use PNG, JPG, JPEG or GIF',
                        'error')
                    return redirect(url_for('edit_team_member', id=id))
                try:
                    member.image_url = handle_file_upload(image)
                except ValueError as e:
                    flash(str(e), 'error')
                    return redirect(url_for('edit_team_member', id=id))

            # Save changes to database
            try:
                db.session.commit()
                flash('Team member updated successfully', 'success')
                return redirect(url_for('admin_team'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating team member: {str(e)}', 'error')
                return redirect(url_for('edit_team_member', id=id))

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('edit_team_member', id=id))

    return render_template('admin/edit_team.html', member=member)


@app.route('/admin/team/<int:id>/delete', methods=['POST'])
@login_required
def delete_team_member(id):
    member = TeamMember.query.get_or_404(id)
    try:
        db.session.delete(member)
        db.session.commit()
        flash('Team member deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting team member: {str(e)}', 'error')
    return redirect(url_for('admin_team'))


@app.route('/admin/gallery/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_gallery_project(id):
    project = GalleryProject.query.get_or_404(id)
    if request.method == 'POST':
        project.title = request.form.get('title', '').strip()
        project.description = request.form.get('description', '').strip()
        project.client = request.form.get('client', '').strip()
        project.category = request.form.get('category', '').strip()
        project.industry_served = request.form.get('industry_served',
                                                   '').strip()
        try:
            project.completion_time = int(
                request.form.get('completion_time', 0))
        except ValueError:
            flash('Invalid completion time value', 'error')
            return redirect(url_for('edit_gallery_project', id=id))

        project.size_category = request.form.get('size_category')
        project.weight_capacity = request.form.get('weight_capacity')
        project.ispm_compliant = bool(request.form.get('ispm_compliant'))
        project.is_featured = bool(request.form.get('is_featured'))

        image = request.files.get('image')
        if image and image.filename:
            if allowed_file(image.filename):
                try:
                    project.image_url = handle_file_upload(
                        image, project.image_url)
                except ValueError as e:
                    flash(str(e), 'error')
                    return redirect(url_for('edit_gallery_project', id=id))
            else:
                flash('Invalid image format. Please use PNG, JPG, JPEG or GIF',
                      'error')
                return redirect(url_for('edit_gallery_project', id=id))

        try:
            db.session.commit()
            flash('Project updated successfully', 'success')
            return redirect(url_for('admin_gallery'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating project: {str(e)}', 'error')
            return redirect(url_for('edit_gallery_project', id=id))

    return render_template('admin/edit_project.html', project=project)


@app.route('/admin/gallery/<int:id>/delete', methods=['POST'])
@login_required
def delete_project(id):
    project = GalleryProject.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully', 'success')
    return redirect(url_for('admin_gallery'))
