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
    category = request.args.get('category')
    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    categories = db.session.query(Product.category).distinct()
    return render_template('products.html',
                         products=products,
                         categories=categories)

@public.route('/quote', methods=['GET', 'POST'])
def quote_calculator():
    if request.method == 'POST':
        # Get form data
        package_type = request.form.get('package_type')
        length = request.form.get('length', '0')
        width = request.form.get('width', '0')
        height = request.form.get('height', '0')
        weight = request.form.get('weight', '0')
        requirements = request.form.getlist('requirements[]')
        shipping_type = request.form.get('shipping_type', 'domestic')

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

        # Configure email settings
        smtp_host = "smtp.mailtrap.io"
        smtp_port = 2525
        smtp_user = os.environ.get('MAILTRAP_USER')
        smtp_pass = os.environ.get('MAILTRAP_PASS')

        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = "New Quote Request - Wood Products Unlimited"
        message['From'] = "quotes@woodproducts.com"
        message['To'] = "chris.candelora@gmail.com"
        
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
