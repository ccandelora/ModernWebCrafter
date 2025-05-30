import os
from flask import Blueprint, render_template, request, send_from_directory, current_app
from models import Product, GalleryProject, Testimonial, TeamMember

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
        
        # Debug log for products
        for product in products:
            print(f"Product: {product.name}")
            print(f"  Description: {product.description}")
            print(f"  Category: {product.category}")
            print(f"  Package Type: {product.package_type}")
            print(f"  Price: {product.price}")
            print(f"  Image URL: {product.image_url}")
        
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

@public.route('/contact')
def contact():
    return render_template('contact.html')

@public.route('/styleguide')
def styleguide():
    """Style guide page showcasing design system components."""
    return render_template('styleguide.html')

@public.route('/robots.txt')
def robots_txt():
    return send_from_directory(current_app.static_folder, 'robots.txt')

@public.route('/sitemap.xml')
def sitemap_xml():
    return send_from_directory(current_app.static_folder, 'sitemap.xml')
