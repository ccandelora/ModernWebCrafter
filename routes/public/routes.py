import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from models import Product, GalleryProject, Testimonial, TeamMember, Inquiry
from app import db

public = Blueprint('public', __name__, template_folder='templates')

@public.route('/')
def index():
    try:
        print("Attempting to render index page")
        featured_products = Product.query.limit(3).all()
        testimonials = Testimonial.query.filter_by(is_featured=True).limit(3).all()
        print("Attempting to fetch featured products and testimonials...")
        print(f"Found {len(featured_products)} products and {len(testimonials)} testimonials")
        
        # Debug products data
        for idx, product in enumerate(featured_products):
            print(f"Product {idx + 1}:")
            print(f"  Name: {product.name}")
            print(f"  Description: {product.description}")
            print(f"  Image URL: {product.image_url}")
            print(f"  Category: {product.category}")
            
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
        # Get form data
        package_type = request.form.get('package_type')
        length = request.form.get('length', '0')
        width = request.form.get('width', '0')
        height = request.form.get('height', '0')
        weight = request.form.get('weight', '0')
        requirements = request.form.getlist('requirements[]')
        shipping_type = request.form.get('shipping_type', 'domestic')
        email = request.form.get('email', '')
        name = request.form.get('name', '')
        phone = request.form.get('phone', '')
        special_instructions = request.form.get('special_instructions', '')

        # Create email content
        package_types = {
            'export_crate': 'ISPM 15 Export Crate',
            'cushioned_crate': 'Cushioned Crate',
            'skidmate': 'Export Skidmate',
            'cushion_skid': 'Cushion Skid with Ramp',
            'oversize': 'Oversize Crate'
        }

        requirement_names = {
            'moisture_barrier': 'Moisture Barrier Protection',
            'shock_absorption': 'Shock Absorption System',
            'custom_foam': 'Custom Foam Interior',
            'ramp_system': 'Loading Ramp System'
        }

        html_content = f"""
        <h2>New Quote Request</h2>
        <h3>Contact Information:</h3>
        <ul>
            <li><strong>Email:</strong> {email}</li>
            {f'<li><strong>Name:</strong> {name}</li>' if name else ''}
            {f'<li><strong>Phone:</strong> {phone}</li>' if phone else ''}
        </ul>
        <h3>Package Details:</h3>
        <ul>
            <li><strong>Package Type:</strong> {package_types.get(package_type, 'Standard Crate')}</li>
            <li><strong>Dimensions:</strong> {length}" × {width}" × {height}"</li>
            <li><strong>Weight:</strong> {weight} lbs</li>
            <li><strong>Shipping Type:</strong> {'International' if shipping_type == 'international' else 'Domestic'}</li>
        </ul>
        """

        if requirements:
            html_content += "<h3>Special Requirements:</h3><ul>"
            for req in requirements:
                html_content += f"<li>{requirement_names.get(req, req)}</li>"
            html_content += "</ul>"
        
        if special_instructions:
            html_content += f"<h3>Special Instructions:</h3><p>{special_instructions}</p>"

        # Configure email settings
        smtp_host = "smtp.mailtrap.io"
        smtp_port = 2525
        smtp_user = os.environ.get('MAILTRAP_USER', '')
        smtp_pass = os.environ.get('MAILTRAP_PASS', '')

        # Validate SMTP credentials
        if not smtp_user or not smtp_pass:
            current_app.logger.error('Missing SMTP credentials')
            flash('Error sending email: Missing SMTP credentials', 'error')
            return redirect(url_for('public.quote_calculator'))

        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = "New Quote Request - Wood Products Unlimited"
        message['From'] = "quotes@woodproducts.com"
        message['To'] = email if email else "chris.candelora@gmail.com"
        
        # Add HTML content
        html_part = MIMEText(html_content, 'html')
        message.attach(html_part)

        try:
            # Send email through Mailtrap
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.login(smtp_user, smtp_pass)
                server.send_message(message)
            flash('Thank you for your quote request! Our team will contact you shortly with pricing details.', 'success')
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
        flash('Thank you for your inquiry! Our team will contact you within 1 business day.',
              'success')
        return redirect(url_for('public.contact'))
    return render_template('contact.html')

@public.route('/styleguide')
def styleguide():
    """Style guide page showcasing design system components."""
    return render_template('styleguide.html')
