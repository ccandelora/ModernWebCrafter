from flask import render_template, request, flash, redirect, url_for
from app import app, db
from models import Product, Inquiry

@app.route('/')
def index():
    featured_products = Product.query.limit(3).all()
    return render_template('index.html', products=featured_products)

@app.route('/products')
def products():
    category = request.args.get('category')
    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    categories = db.session.query(Product.category).distinct()
    return render_template('products.html', products=products, categories=categories)

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

@app.context_processor
def utility_processor():
    def get_categories():
        return db.session.query(Product.category).distinct()
    return dict(get_categories=get_categories)
