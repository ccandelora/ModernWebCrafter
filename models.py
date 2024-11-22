from extensions import db
from flask_login import UserMixin
from datetime import datetime

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TeamMember(db.Model):
    __tablename__ = 'team_members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class GalleryProject(db.Model):
    __tablename__ = 'gallery_projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    industry = db.Column(db.String(50))
    size = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completion_date = db.Column(db.DateTime)
    category = db.Column(db.String(50))
    industry_served = db.Column(db.String(50))
    size_category = db.Column(db.String(50))


    def __repr__(self):
        return f'<GalleryProject {self.title}>'

class Testimonial(db.Model):
    __tablename__ = 'testimonials'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # Optional: for star ratings
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def init_gallery_projects():
    if GalleryProject.query.count() == 0:
        projects = [
            GalleryProject(
                title="Custom Shipping Crates",
                description="Heavy-duty shipping crates for industrial equipment",
                image_url="/static/images/projects/crates.jpg",
                industry="shipping",
                size="large"
            ),
            GalleryProject(
                title="Export Packaging",
                description="ISPM-15 certified export packaging solutions",
                image_url="/static/images/projects/export.jpg",
                industry="export",
                size="medium"
            ),
            # Add more sample projects as needed
        ]
        
        for project in projects:
            db.session.add(project)
        db.session.commit()