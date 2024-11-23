from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Product, GalleryProject, Testimonial, Inquiry, TeamMember
from app import db

public = Blueprint('public', __name__, template_folder='templates')

@public.route('/')
def index():
    try:
        print("Attempting to render index page")
        featured_products = Product.query.limit(3).all()
        testimonials = Testimonial.query.filter_by(is_featured=True).limit(3).all()
        print(f"Found {len(featured_products)} products and {len(testimonials)} testimonials")
        return render_template('index.html',
                             products=featured_products,
                             testimonials=testimonials)
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
        length = float(request.form.get('length', 0))
        width = float(request.form.get('width', 0))
        height = float(request.form.get('height', 0))
        weight = float(request.form.get('weight', 0))
        requirements = request.form.getlist('requirements[]')
        shipping_type = request.form.get('shipping_type')

        # Calculate cubic feet
        cubic_feet = (length * width * height) / 1728  # Convert cubic inches to cubic feet

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
        weight_factor = max(1.0, weight / 1000)  # Increase cost for heavy items
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
