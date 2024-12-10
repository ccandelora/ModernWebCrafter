import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from models import GalleryProject

def check_paths():
    app = create_app()
    with app.app_context():
        projects = GalleryProject.query.all()
        print("\nStored image paths:")
        for project in projects:
            print(f"Title: {project.title}")
            print(f"Image URL: {project.image_url}")
            print("---")

if __name__ == "__main__":
    check_paths() 