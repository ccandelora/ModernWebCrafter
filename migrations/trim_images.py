import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from models import GalleryProject
from routes.utils.upload import trim_whitespace, handle_file_upload
from PIL import Image
import io

def trim_existing_images():
    app = create_app()
    with app.app_context():
        try:
            # Get all gallery projects
            projects = GalleryProject.query.all()
            
            for project in projects:
                if not project.image_url:
                    continue
                    
                # Get the full path of the image
                image_path = os.path.join('.', project.image_url.lstrip('/'))
                
                if not os.path.exists(image_path):
                    print(f"Image not found: {image_path}")
                    continue
                
                try:
                    # Open and process the image
                    with Image.open(image_path) as img:
                        # Convert to RGB if needed
                        if img.mode in ('RGBA', 'LA', 'P'):
                            img = img.convert('RGB')
                        
                        # Trim white spaces
                        trimmed_img = trim_whitespace(img)
                        
                        # Save the trimmed image back to a buffer
                        img_buffer = io.BytesIO()
                        trimmed_img.save(img_buffer, format='WEBP', quality=85, method=6)
                        img_buffer.seek(0)
                        
                        # Create a file-like object from the buffer
                        from werkzeug.datastructures import FileStorage
                        file = FileStorage(
                            stream=img_buffer,
                            filename=os.path.basename(image_path)
                        )
                        
                        # Use the existing upload handler to process and save the image
                        result = handle_file_upload(file, old_file_path=project.image_url)
                        
                        # Update the project's image URL
                        if isinstance(result, dict):
                            project.image_url = result['original']
                        else:
                            project.image_url = result
                            
                        db.session.commit()
                        print(f"Successfully processed image for project: {project.title}")
                        
                except Exception as e:
                    print(f"Error processing image for project {project.title}: {str(e)}")
                    continue
            
            print("Image trimming process completed")
            
        except Exception as e:
            print(f"Error during image trimming: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    trim_existing_images() 