import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from models import GalleryProject

def update_image_paths():
    app = create_app()
    with app.app_context():
        try:
            # Get all gallery projects
            projects = GalleryProject.query.all()
            
            for project in projects:
                # Skip if image_url is already correct
                if project.image_url.startswith('/static/images/uploads/'):
                    continue
                    
                # Convert path to original format
                if '/uploads/' in project.image_url:
                    # Remove any variant suffixes
                    base_path = project.image_url.replace('_large', '').replace('_medium', '').replace('_small', '')
                    # Ensure the path starts with /static/
                    if not base_path.startswith('/static/'):
                        base_path = '/static' + base_path
                    project.image_url = base_path
            
            # Commit changes
            db.session.commit()
            print("Successfully updated image paths")
            
        except Exception as e:
            print(f"Error updating image paths: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    update_image_paths() 