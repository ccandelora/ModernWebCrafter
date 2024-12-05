import os
import logging
from PIL import Image, ImageFilter, ImageOps
import io
from werkzeug.utils import secure_filename

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
        dict: Dictionary containing paths to original and variant images
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
            
        # Get original dimensions and orientation
        width, height = img.size
        is_vertical = height > width
        aspect_ratio = height / width if is_vertical else width / height
        
        logging.info(f"Original dimensions: {width}x{height}, Vertical: {is_vertical}, Aspect ratio: {aspect_ratio:.2f}")
        
        # Set standard dimensions for all images
        standard_size = (1000, 1000)  # Larger fixed square size for better quality
        
        # Create a new white background image
        new_img = Image.new('RGB', standard_size, 'white')
        
        # Add padding (10% of the standard size)
        padding = int(standard_size[0] * 0.1)
        max_content_size = (standard_size[0] - 2 * padding, standard_size[1] - 2 * padding)
        
        # Calculate scaling to fit within padded area while preserving aspect ratio
        scale = min(max_content_size[0] / width, max_content_size[1] / height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Resize original image
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Calculate position to center the image
        left = (standard_size[0] - new_width) // 2
        top = (standard_size[1] - new_height) // 2
        
        # Paste the resized image onto the white background
        new_img.paste(img, (left, top))
        img = new_img
        
        # Add a subtle border
        img = ImageOps.expand(img, border=2, fill='#f0f0f0')
        
        logging.info(f"Standardized to {standard_size[0]}x{standard_size[1]}, maintained aspect ratio with padding")
            
    except (IOError, OSError) as e:
        logging.warning(f"Invalid image file format: {str(e)}")
        raise ValueError('Invalid image format. Please upload a JPG, PNG, or WebP file.')
    except Exception as e:
        logging.warning(f"Error processing image file: {str(e)}")
        raise ValueError('Error processing image. Please try again with a different file.')

    # Ensure upload directory exists
    upload_dir = ensure_upload_dir()
    variants_dir = os.path.join(upload_dir, 'variants')
    os.makedirs(variants_dir, exist_ok=True)

    try:
        # Create secure filename
        secure_name = secure_filename(file.filename)
        base_name, ext = os.path.splitext(secure_name)
        webp_name = f"{base_name}.webp"
        relative_path = os.path.join('static', 'images', 'uploads', webp_name)
        full_path = os.path.join('.', relative_path)

        # Save the original optimized image
        img.save(full_path, 'WEBP', quality=85, method=6)
        
        # Generate variants with proper aspect ratio preservation
        # Define maximum dimensions for variants while maintaining aspect ratio
        variant_max_sizes = {
            'large': 1200,
            'medium': 800,
            'small': 400,
            'thumbnail': 200
        }
        
        variant_paths = {}
        for size_name, max_dimension in variant_max_sizes.items():
            variant = img.copy()
            
            # Calculate scaling factor for variant while preserving aspect ratio
            scale = 1.0
            if width > max_dimension or height > max_dimension:
                scale = max_dimension / max(width, height)
            
            # Calculate variant dimensions
            var_width = int(width * scale)
            var_height = int(height * scale)
                
            # Resize variant
            variant = variant.resize((var_width, var_height), Image.Resampling.LANCZOS)
            
            # Save WebP variant
            variant_filename = f"{base_name}_{size_name}.webp"
            variant_path = os.path.join(variants_dir, variant_filename)
            variant.save(variant_path, 'WEBP', quality=85, method=6)
            
            # Save JPEG fallback
            jpeg_filename = f"{base_name}_{size_name}.jpg"
            jpeg_path = os.path.join(variants_dir, jpeg_filename)
            variant.save(jpeg_path, 'JPEG', quality=85, optimize=True)
            
            # Store relative path for variant
            variant_paths[size_name] = '/' + os.path.relpath(variant_path, '.')

        # Clean up old file if it exists
        if old_file_path and 'placeholder' not in old_file_path:
            try:
                old_full_path = os.path.join('.', old_file_path.lstrip('/'))
                if os.path.exists(old_full_path):
                    os.remove(old_full_path)
                    logging.info(f"Removed old file: {old_full_path}")
            except Exception as e:
                logging.warning(f"Failed to remove old file: {str(e)}")

        # Return paths dictionary
        return {
            'original': '/' + relative_path,
            'variants': variant_paths
        }

    except Exception as e:
        logging.error(f"Error saving file {secure_name}: {str(e)}")
        raise ValueError(f'Error saving file: {str(e)}')

# Ensure upload directory exists at startup
ensure_upload_dir()