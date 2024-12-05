import os
import logging
from PIL import Image, ImageFilter
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
    base_name, ext = os.path.splitext(secure_name)
    webp_name = f"{base_name}.webp"
    relative_path = os.path.join('static', 'images', 'uploads', webp_name)
    full_path = os.path.join('.', relative_path)

    try:
        # Open and process the image using PIL
        img = Image.open(file)
        
        # Strip EXIF data for privacy and size reduction
        data = list(img.getdata())
        image_without_exif = Image.new(img.mode, img.size)
        image_without_exif.putdata(data)
        img = image_without_exif
        
        # Convert color mode if needed
        if img.mode in ('RGBA', 'LA'):
            background = Image.new(img.mode[:-1], img.size, (255, 255, 255))
            background.paste(img, img.split()[-1])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Calculate new dimensions optimized for product cards
        width, height = img.size
        target_width = 800  # Base width for product cards
        target_height = 600  # Base height for product cards
        
        # Calculate aspect ratio
        aspect_ratio = width / height
        
        if aspect_ratio > 1:  # Landscape
            new_width = min(width, target_width)
            new_height = int(new_width / aspect_ratio)
            if new_height > target_height:
                new_height = target_height
                new_width = int(new_height * aspect_ratio)
        else:  # Portrait
            new_height = min(height, target_height)
            new_width = int(new_height * aspect_ratio)
            if new_width > target_width:
                new_width = target_width
                new_height = int(new_width / aspect_ratio)
        
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        logging.info(f"Resized image to {new_width}x{new_height} (aspect ratio: {aspect_ratio:.2f})")
        
        # Create a white background image with consistent dimensions
        background = Image.new('RGB', (target_width, target_height), 'white')
        # Calculate position to center the image
        x = (target_width - new_width) // 2
        y = (target_height - new_height) // 2
        # Paste the resized image onto the background
        background.paste(img, (x, y))
        img = background
        
        # Apply subtle sharpening after resize
        img = img.filter(ImageFilter.SHARPEN)
        
        # Save main WebP version
        webp_path = full_path
        img.save(webp_path, 'WEBP', quality=85, method=6, lossless=False)
        
        # If file size is too large, gradually reduce quality for WebP
        if os.path.getsize(webp_path) > max_size_mb * 1024 * 1024:
            for quality in [75, 65, 55]:
                img.save(webp_path, 'WEBP', quality=quality, method=6, lossless=False)
                if os.path.getsize(webp_path) <= max_size_mb * 1024 * 1024:
                    break
        
        # Save fallback version in JPEG format
        fallback_name = f"{base_name}.jpg"
        fallback_path = os.path.join('.', 'static', 'images', 'uploads', fallback_name)
        img.save(fallback_path, 'JPEG', quality=85, optimize=True)
        
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
