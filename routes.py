from flask import render_template, request, flash, redirect, url_for
from app import app, db
from models import Product, Inquiry, Testimonial, GalleryProject
from datetime import date
import json

@app.route('/')
def index():
    featured_products = Product.query.limit(3).all()
    testimonials = Testimonial.query.filter_by(is_featured=True).limit(3).all()
    return render_template('index.html', products=featured_products, testimonials=testimonials)

@app.route('/products')
def products():
    category = request.args.get('category')
    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    categories = db.session.query(Product.category).distinct()
    return render_template('products.html', products=products, categories=categories)

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
        inquiry = Inquiry(
            name=request.form['name'],
            email=request.form['email'],
            message=request.form['message']
        )
        if 'product_id' in request.form:
            inquiry.product_id = request.form['product_id']
        
        db.session.add(inquiry)
        db.session.commit()
        flash('Your inquiry has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/admin/testimonials', methods=['GET', 'POST'])
def manage_testimonials():
    if request.method == 'POST':
        testimonial = Testimonial(
            client_name=request.form['client_name'],
            rating=int(request.form['rating']),
            content=request.form['content'],
            is_featured=bool(request.form.get('is_featured', False))
        )
        db.session.add(testimonial)
        db.session.commit()
        flash('Testimonial added successfully!', 'success')
        return redirect(url_for('manage_testimonials'))
    
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('admin/testimonials.html', testimonials=testimonials)

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
