from app import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(100))
    industry = db.Column(db.String(50))
    package_type = db.Column(db.String(50))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class GalleryProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    completion_date = db.Column(db.Date, nullable=False)
    completion_time = db.Column(db.Integer)  # In days
    client = db.Column(db.String(100))
    category = db.Column(db.String(50), nullable=False)
    industry_served = db.Column(db.String(50))
    size_category = db.Column(db.String(50))  # Small, Medium, Large, Oversize
    weight_capacity = db.Column(db.String(50))  # Weight capacity specification
    ispm_compliant = db.Column(db.Boolean, default=False)  # International shipping compliance
    special_features = db.Column(db.Text)  # JSON string of special features
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
