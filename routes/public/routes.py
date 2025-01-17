import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from models import Product, GalleryProject, Testimonial, TeamMember, Inquiry
from app import db
from routes.utils.email import send_contact_email, send_quote_email, send_test_email

public = Blueprint('public', __name__, template_folder='templates')

@public.route('/')
def index():
    try:
        print("Attempting to render index page")
        featured_products = Product.query.filter_by(is_featured=True).all()
        testimonials = Testimonial.query.filter_by(is_featured=True).all()
        print("Attempting to fetch featured products and testimonials...")
        print(f"Found {len(featured_products)} products and {len(testimonials)} testimonials")
        
        # Debug products data
        for idx, product in enumerate(featured_products):
            print(f"Product {idx + 1}:")
            print(f"  Name: {product.name}")
            print(f"  Description: {product.description}")
            print(f"  Image URL: {product.image_url}")
            print(f"  Category: {product.category}")
            print(f"  Featured: {product.is_featured}")
            
        # Debug testimonials data
        for idx, testimonial in enumerate(testimonials):
            print(f"Testimonial {idx + 1}:")
            print(f"  Client Name: {testimonial.client_name}")
            print(f"  Rating: {testimonial.rating}")
            print(f"  Content: {testimonial.content}")
            print(f"  Featured: {testimonial.is_featured}")
            
        hero_variant = request.args.get('hero', '1')
        return render_template('index.html',
                             products=featured_products,
                             testimonials=testimonials,
                             hero_variant=hero_variant)
    except Exception as e:
        print(f"Error in index route: {str(e)}")
        return str(e), 500

@public.route('/about')
def about():
    team_members = TeamMember.query.filter_by(is_active=True).order_by(
        TeamMember.order.asc()).all()
    return render_template('about.html', team_members=team_members)

@public.route('/products')
def products():
    try:
        # Get all products, sorted alphabetically by name
        products = Product.query.order_by(Product.name.asc()).all()
        
        # Get unique categories while maintaining alphabetical order of products
        categories = sorted(set(p.category for p in products if p.category))
        
        return render_template('products.html', 
                             products=products,
                             categories=categories)
    except Exception as e:
        print(f"Error in products route: {str(e)}")
        flash('Error loading products. Please try again later.', 'error')
        return render_template('products.html', 
                             products=[],
                             categories=[])

@public.route('/quote', methods=['GET', 'POST'])
def quote_calculator():
    # Pre-fill form data from URL parameters
    product_data = {
        'package_type': request.args.get('package_type', ''),
        'name': request.args.get('name', ''),
        'description': request.args.get('description', '')
    }
    
    if request.method == 'POST':
        try:
            # Get form data
            form_data = {
                'package_type': request.form.get('package_type'),
                'length': request.form.get('length', '0'),
                'width': request.form.get('width', '0'),
                'height': request.form.get('height', '0'),
                'weight': request.form.get('weight', '0'),
                'requirements': request.form.getlist('requirements[]'),
                'shipping_type': request.form.get('shipping_type', 'domestic'),
                'email': request.form.get('email', ''),
                'name': request.form.get('name', ''),
                'phone': request.form.get('phone', ''),
                'special_instructions': request.form.get('special_instructions', '')
            }

            # Send email
            send_quote_email(form_data)
            flash('Thank you for your quote request! Our team will contact you within 1 business day.', 'success')
        except Exception as e:
            current_app.logger.error(f'Error sending email: {str(e)}')
            flash('There was an error processing your request. Please try again or contact us directly.', 'error')

        return redirect(url_for('public.quote_calculator'))

    return render_template('quote.html')

@public.route('/gallery')
def gallery():
    category = request.args.get('category')
    industry = request.args.get('industry')
    size = request.args.get('size')

    # Base query
    query = GalleryProject.query

    # Apply filters
    if category:
        query = query.filter_by(category=category)
    if industry:
        query = query.filter_by(industry_served=industry)
    if size:
        query = query.filter_by(size_category=size)

    # Get filtered projects
    projects = query.order_by(GalleryProject.completion_date.desc()).all()

    # Get all distinct values and their counts
    all_projects = GalleryProject.query.all()
    
    # Get categories with counts
    categories_dict = {}
    for p in all_projects:
        if p.category:
            categories_dict[p.category] = categories_dict.get(p.category, 0) + 1
    categories = [(cat, count) for cat, count in categories_dict.items()]
    categories.sort(key=lambda x: x[0])  # Sort by category name

    # Get industries with counts
    industries_dict = {}
    for p in all_projects:
        if p.industry_served:
            industries_dict[p.industry_served] = industries_dict.get(p.industry_served, 0) + 1
    industries = [(ind, count) for ind, count in industries_dict.items()]
    industries.sort(key=lambda x: x[0])  # Sort by industry name

    # Get sizes with counts
    sizes_dict = {}
    for p in all_projects:
        if p.size_category:
            sizes_dict[p.size_category] = sizes_dict.get(p.size_category, 0) + 1
    sizes = [(size, count) for size, count in sizes_dict.items()]
    sizes.sort(key=lambda x: x[0])  # Sort by size name

    return render_template('gallery.html',
                         projects=projects,
                         categories=categories,
                         industries=industries,
                         sizes=sizes,
                         selected_category=category,
                         selected_industry=industry,
                         selected_size=size)

@public.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            # Log the form data (excluding sensitive info)
            current_app.logger.info('Processing contact form submission')
            current_app.logger.debug(f'Form data: name={request.form.get("name")}, '
                                   f'company={request.form.get("company")}, '
                                   f'industry={request.form.get("industry")}, '
                                   f'package_type={request.form.get("package_type")}')

            # Create new inquiry with additional fields
            inquiry = Inquiry(name=request.form['name'],
                            email=request.form['email'],
                            company=request.form.get('company', ''),
                            industry=request.form.get('industry', ''),
                            package_type=request.form.get('package_type', ''),
                            message=request.form['message'])
            if 'product_id' in request.form:
                inquiry.product_id = request.form['product_id']

            current_app.logger.info('Saving inquiry to database')
            db.session.add(inquiry)
            db.session.commit()
            current_app.logger.info('Inquiry saved successfully')

            # Send email
            current_app.logger.info('Attempting to send contact email')
            send_contact_email(request.form)
            flash('Thank you for your inquiry! Our team will contact you within 1 business day.', 'success')
            
        except Exception as e:
            db.session.rollback()
            error_msg = str(e)
            current_app.logger.error(f'Error processing contact form: {error_msg}')
            current_app.logger.exception('Full traceback:')
            
            # Show a more detailed error message in development
            if current_app.debug:
                flash(f'Error: {error_msg}', 'error')
            else:
                flash('There was an error processing your request. Please try again or contact us directly.', 'error')

        return redirect(url_for('public.contact'))
    return render_template('contact.html')

@public.route('/styleguide')
def styleguide():
    """Style guide page showcasing design system components."""
    return render_template('styleguide.html')

@public.route('/test-email')
def test_email():
    try:
        current_app.logger.info('Starting test email process')
        success, message = send_test_email()
        
        if success:
            current_app.logger.info('Test email sent successfully')
            flash('Test email sent successfully!', 'success')
        else:
            current_app.logger.error(f'Test email failed: {message}')
            # In debug mode, show the actual error
            if current_app.debug:
                flash(f'Error sending test email: {message}', 'error')
            else:
                flash('Error sending test email. Please check the server logs.', 'error')
    except Exception as e:
        current_app.logger.error(f'Exception in test email route: {str(e)}')
        current_app.logger.exception('Full traceback:')
        if current_app.debug:
            flash(f'Error: {str(e)}', 'error')
        else:
            flash('An unexpected error occurred. Please check the server logs.', 'error')
    
    return redirect(url_for('public.contact'))
