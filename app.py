import os
from flask import Flask
from extensions import db, login_manager, csrf
from datetime import datetime
from models import GalleryProject, User
from routes.main import main_bp
from routes.admin import admin
from routes.admin.product_routes import products_bp
from routes.auth import auth_bp
from routes.public.routes import public

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY") or "woodcraft_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///woodproducts.db"
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['DEBUG'] = True
    app.config['WTF_CSRF_ENABLED'] = True

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Add user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Add context processor for datetime
    @app.context_processor
    def utility_processor():
        return {
            'now': datetime.utcnow
        }

    with app.app_context():
        # Import blueprints
        from routes.public.routes import public
        from routes.admin import admin
        from routes.admin.product_routes import products_bp
        from routes.auth import auth_bp
        
        # Register blueprints with explicit template folders
        app.register_blueprint(public)  # Register at root level
        app.register_blueprint(admin, url_prefix='/admin')
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(products_bp, url_prefix='/admin/products')
        
        # Initialize database
        db.create_all()
        
    return app

def init_db(app):
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Add sample gallery projects if none exist
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
                GalleryProject(
                    title="Custom Pallets",
                    description="Custom-designed pallets for unique shipping needs",
                    image_url="/static/images/projects/pallets.jpg",
                    industry="shipping",
                    size="medium"
                )
            ]
            
            for project in projects:
                db.session.add(project)
            db.session.commit()
            print("Added sample gallery projects")

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

