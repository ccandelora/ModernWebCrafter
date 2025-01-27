import os
import logging
from PIL import Image, ImageFilter, ImageOps, ImageDraw
import io
from werkzeug.utils import secure_filename
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
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
    Handle file upload with advanced image optimization
    Args:
        file: FileStorage object from request.files
        old_file_path: Optional path to old file that should be removed
        max_size_mb: Maximum file size in MB (default 5MB)
        max_dimension: Maximum image dimension (width/height) in pixels
    Returns:
        str: Path to the uploaded image
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

    try:
        # Create a copy of the file content for validation
        img_copy = io.BytesIO(file_content)
        img = Image.open(img_copy)
        
        # Convert to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
            
        # Get original dimensions
        width, height = img.size
        aspect_ratio = height / width
        
        logging.info(f"Original dimensions: {width}x{height}, Aspect ratio: {aspect_ratio:.2f}")
        
        # Calculate new dimensions while preserving aspect ratio
        if width > max_dimension or height > max_dimension:
            if width > height:
                new_width = max_dimension
                new_height = int(max_dimension * aspect_ratio)
            else:
                new_height = max_dimension
                new_width = int(max_dimension / aspect_ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            logging.info(f"Resized to {new_width}x{new_height}")
        
        # Add a subtle border
        img = ImageOps.expand(img, border=2, fill='#f0f0f0')

        # Ensure upload directory exists
        upload_dir = ensure_upload_dir()

        try:
            # Create secure filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            secure_name = secure_filename(file.filename)
            base_name, ext = os.path.splitext(secure_name)
            webp_name = f"{base_name}_{timestamp}.webp"
            relative_path = os.path.join('static', 'images', 'uploads', webp_name)
            full_path = os.path.join('.', relative_path)

            # Save the processed image
            img.save(full_path, 'WEBP', quality=85, method=6)

            # Clean up old file if it exists
            if old_file_path and 'placeholder' not in old_file_path:
                try:
                    old_full_path = os.path.join('.', old_file_path.lstrip('/'))
                    if os.path.exists(old_full_path):
                        os.remove(old_full_path)
                        logging.info(f"Removed old file: {old_full_path}")
                except Exception as e:
                    logging.warning(f"Failed to remove old file: {str(e)}")

            # Return only the relative path
            path_str = '/' + relative_path
            logging.info(f"Returning image path: {path_str}")
            return path_str

        except Exception as e:
            logging.error(f"Error saving file {secure_name}: {str(e)}")
            raise ValueError(f'Error saving file: {str(e)}')

    except (IOError, OSError) as e:
        logging.warning(f"Invalid image file format: {str(e)}")
        raise ValueError('Invalid image format. Please upload a JPG, PNG, or WebP file.')
    except Exception as e:
        logging.warning(f"Error processing image file: {str(e)}")
        raise ValueError('Error processing image. Please try again with a different file.')

def handle_team_photo_upload(file, old_file_path=None, max_size_mb=5):
    """
    Handle team member photo upload with circular cropping
    Args:
        file: FileStorage object from request.files
        old_file_path: Optional path to old file that should be removed
        max_size_mb: Maximum file size in MB (default 5MB)
    Returns:
        str: Path to the uploaded image
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

    try:
        # Create a copy of the file content for validation
        img_copy = io.BytesIO(file_content)
        img = Image.open(img_copy)
        
        # Convert to RGBA to support transparency
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            
        # Create a square image with the shorter dimension
        size = min(img.size)
        
        # Calculate crop box for center crop
        left = (img.width - size) // 2
        top = (img.height - size) // 2
        right = left + size
        bottom = top + size
        
        # Crop to square
        img = img.crop((left, top, right, bottom))
        
        # Create circular mask
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        
        # Create output image with transparent background
        output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        output.paste(img, (0, 0))
        output.putalpha(mask)
        
        # Resize to standard size (800x800)
        standard_size = (800, 800)
        output = output.resize(standard_size, Image.Resampling.LANCZOS)
        
        logging.info(f"Processed team photo to {standard_size[0]}x{standard_size[1]} circular format")
            
    except (IOError, OSError) as e:
        logging.warning(f"Invalid image file format: {str(e)}")
        raise ValueError('Invalid image format. Please upload a JPG, PNG, or WebP file.')
    except Exception as e:
        logging.warning(f"Error processing image file: {str(e)}")
        raise ValueError('Error processing image. Please try again with a different file.')

    # Ensure upload directory exists
    upload_dir = ensure_upload_dir()

    try:
        # Create secure filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        secure_name = secure_filename(file.filename)
        base_name, ext = os.path.splitext(secure_name)
        webp_name = f"{base_name}_{timestamp}.webp"
        relative_path = os.path.join('static', 'images', 'uploads', webp_name)
        full_path = os.path.join('.', relative_path)

        # Save the processed image
        output.save(full_path, 'WEBP', quality=85, method=6)

        # Clean up old file if it exists
        if old_file_path and 'placeholder' not in old_file_path:
            try:
                old_full_path = os.path.join('.', old_file_path.lstrip('/'))
                if os.path.exists(old_full_path):
                    os.remove(old_full_path)
                    logging.info(f"Removed old file: {old_full_path}")
            except Exception as e:
                logging.warning(f"Failed to remove old file: {str(e)}")

        # Return only the relative path
        path_str = '/' + relative_path
        logging.info(f"Returning team photo path: {path_str}")
        return path_str

    except Exception as e:
        logging.error(f"Error saving file {secure_name}: {str(e)}")
        raise ValueError(f'Error saving file: {str(e)}')

# Ensure upload directory exists at startup
ensure_upload_dir()