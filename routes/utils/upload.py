import os
import logging
from PIL import Image
import io
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = os.path.join('static', 'images', 'uploads')

def allowed_file(filename):
    if not filename:
        return False
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_dir():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    return UPLOAD_FOLDER

def handle_file_upload(file, old_file_path=None, max_size_mb=5, max_dimension=2000):
    """
    Handle file upload with proper path handling, size and dimension verification
    Args:
        file: FileStorage object from request.files
        old_file_path: Optional path to old file that should be removed
        max_size_mb: Maximum file size in MB (default 5MB)
        max_dimension: Maximum image dimension (width/height) in pixels
    Returns:
        str: URL path to the saved file (with leading slash)
    Raises:
        ValueError: If file validation or saving fails
    """
    if not file or not file.filename:
        logging.warning("No file provided for upload")
        raise ValueError('No file provided')

    # Check file size
    file_content = file.read()
    file_size_mb = len(file_content) / (1024 * 1024)  # Convert to MB
    if file_size_mb > max_size_mb:
        logging.warning(f"File too large: {file_size_mb}MB")
        raise ValueError(f'File size exceeds {max_size_mb}MB limit')

    # Reset file pointer for further processing
    file.seek(0)

    if not allowed_file(file.filename):
        logging.warning(f"Invalid file format: {file.filename}")
        raise ValueError('Invalid file format. Please use PNG, JPG, JPEG or GIF')

    # Validate image dimensions and format using PIL
    try:
        img = Image.open(io.BytesIO(file_content))
        width, height = img.size
        
        if width > max_dimension or height > max_dimension:
            logging.warning(f"Image dimensions too large: {width}x{height}")
            raise ValueError(f'Image dimensions exceed {max_dimension}x{max_dimension} pixels limit')
            
        # Verify it's a valid image format
        img.verify()
    except Exception as e:
        logging.warning(f"Invalid image file: {str(e)}")
        raise ValueError('Invalid image file. Please upload a valid image.')

    # Reset file pointer after validation
    file.seek(0)

    # Ensure upload directory exists
    upload_dir = ensure_upload_dir()
    logging.info(f"Using upload directory: {upload_dir}")

    # Create secure filename and construct proper paths
    secure_name = secure_filename(file.filename)
    relative_path = os.path.join('static', 'images', 'uploads', secure_name)
    full_path = os.path.join('.', relative_path)

    try:
        # Open and compress the image using PIL
        img = Image.open(file)
        
        # Convert to RGB if image is in RGBA mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')
            
        # Calculate new dimensions while maintaining aspect ratio
        width, height = img.size
        max_size = 1200  # Maximum dimension for compressed images
        
        if width > max_size or height > max_size:
            if width > height:
                new_width = max_size
                new_height = int((height / width) * max_size)
            else:
                new_height = max_size
                new_width = int((width / height) * max_size)
            img = img.resize((new_width, new_height), Image.LANCZOS)
            logging.info(f"Resized image to {new_width}x{new_height}")
            
        # Save with compression
        img.save(full_path, optimize=True, quality=85)
        
        if not os.path.exists(full_path):
            logging.error(f"Failed to save file to {full_path}")
            raise ValueError("Failed to save the file")
            
        logging.info(f"Successfully saved compressed file to {full_path}")

        # Handle old file removal if exists
        if old_file_path and 'avatar-placeholder.svg' not in old_file_path:
            try:
                old_full_path = os.path.join('.', old_file_path.lstrip('/'))
                if os.path.exists(old_full_path):
                    os.remove(old_full_path)
                    logging.info(f"Removed old file: {old_full_path}")
            except Exception as e:
                logging.warning(f"Failed to remove old file {old_full_path}: {str(e)}")

        # Return the path relative to static folder, with leading slash
        return '/' + relative_path
    except Exception as e:
        logging.error(f"Error saving file {secure_name}: {str(e)}")
        raise ValueError(f'Error saving file: {str(e)}')

# Ensure upload directory exists at startup
ensure_upload_dir()
