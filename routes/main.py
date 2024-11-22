from flask import Blueprint, render_template, request
from extensions import db
from models import GalleryProject

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/products')
def products():
    return render_template('products.html')

@main_bp.route('/quote-calculator')
def quote_calculator():
    return render_template('quote_calculator.html')

@main_bp.route('/gallery')
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
    

@main_bp.route('/contact')
def contact():
    return render_template('contact.html') 