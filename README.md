# Wood Products Unlimited - Industrial Wood Packaging Solutions

A comprehensive web platform for a wood products business featuring a product catalog, inquiry system, and project gallery. Built with Flask, Tailwind CSS, and modern web technologies.

## Features

- 🏭 Product Catalog with Industrial Packaging Solutions
- 🧮 Multi-step Quote Calculator with International Shipping Support
- 🖼️ Dynamic Project Gallery with Filtering
- 📱 Mobile-First Responsive Design
- 🔍 SEO-Optimized Content
- ✨ Interactive UI Components
- 📊 NELMA and ISPM 15 Certification Integration
- 🗺️ Google Maps Integration

## Tech Stack

- **Backend**: Python/Flask
- **Frontend**: Tailwind CSS, Custom CSS
- **Database**: SQLite with SQLAlchemy ORM
- **JavaScript**: Vanilla JS for interactive components
- **SVG Graphics**: Custom wood-themed design elements

## Prerequisites

- Python 3.11+
- Node.js and npm (for Tailwind CSS)
- Git

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd wood-products-website
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Node.js dependencies:
```bash
npm install
```

4. Build Tailwind CSS:
```bash
npx tailwindcss -i ./static/css/src/input.css -o ./static/css/tailwind.css
```

5. Set up environment variables:
```bash
FLASK_SECRET_KEY=your_secret_key
```

## Local Development Setup

### Admin Account Setup

1. Create an admin user:
```bash
# Start Python shell
python
>>> from app import app, db
>>> from models import Admin
>>> with app.app_context():
...     admin = Admin(username='admin', email='admin@example.com')
...     admin.set_password('your-secure-password')
...     db.session.add(admin)
...     db.session.commit()
```

2. Access admin interface:
- Navigate to `/admin/login`
- Login with admin credentials
- Access admin dashboard at `/admin`

### Database Setup

1. SQLite Database Initialization:
```bash
# The database will be automatically created in instance/woodproducts.db
# Ensure the instance directory exists
mkdir instance
```

2. Schema Creation:
```bash
# Start Python shell
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
```

3. Sample Data Population:
```bash
# The sample data will be automatically populated when running the application
# This includes:
# - Product catalog entries
# - Sample testimonials
# - Gallery projects
# You can modify the sample data in app.py
```

### Local Server Configuration

1. Environment Variables Setup:
```bash
# Create a .env file in the project root
FLASK_APP=main.py
FLASK_ENV=development
FLASK_SECRET_KEY=your_secret_key
FLASK_DEBUG=1

# Optional environment variables
DATABASE_URL=sqlite:///instance/woodproducts.db
PORT=5000
```

2. Port Configuration:
- Default port is 5000
- Can be modified in main.py or through environment variables
- To use a different port:
```python
# In main.py
app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
```

3. Debug Mode Settings:
```bash
# Enable debug mode for development
export FLASK_DEBUG=1

# Or in Python code (main.py)
app.config['DEBUG'] = True
```

### Running the Application

1. Database Initialization:
```bash
# The database will be automatically initialized when starting the application
# You can manually initialize it using:
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
```

2. Tailwind CSS Compilation:
```bash
# One-time build
npx tailwindcss -i ./static/css/src/input.css -o ./static/css/tailwind.css

# Watch mode for development
npx tailwindcss -i ./static/css/src/input.css -o ./static/css/tailwind.css --watch
```

3. Flask Server Startup:
```bash
# Start the Flask development server
python main.py
```

4. Accessing the Local Site:
- Open your browser and navigate to: http://localhost:5000
- The site will be available at http://0.0.0.0:5000 for external access

### Troubleshooting

#### Database Connection Issues

1. Database File Permission Problems:
```bash
# Check instance directory permissions
chmod 755 instance
chmod 644 instance/woodproducts.db
```

2. SQLite Database Lock Errors:
- Ensure only one application instance is running
- Check for hanging database connections
- Verify write permissions in the instance directory

3. Schema Mismatch:
```bash
# Reset the database
rm instance/woodproducts.db
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
```

#### CSS Compilation Problems

1. Tailwind Build Failures:
```bash
# Clear the CSS cache
rm static/css/tailwind.css

# Reinstall node modules
rm -rf node_modules
npm install

# Rebuild Tailwind CSS
npx tailwindcss -i ./static/css/src/input.css -o ./static/css/tailwind.css
```

2. Missing CSS Dependencies:
```bash
# Verify package.json configuration
npm install tailwindcss postcss autoprefixer

# Update Tailwind configuration
npx tailwindcss init -p
```

#### Port Conflicts

1. Address Already in Use:
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use a different port
export PORT=5001
```

2. Permission Issues:
- Use ports > 1024 for development
- Run the application without sudo
- Configure proper user permissions

#### Dependencies Issues

1. Python Package Conflicts:
```bash
# Clear Python cache
find . -type d -name "__pycache__" -exec rm -r {} +

# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

2. Node.js Version Conflicts:
```bash
# Use recommended Node.js version
nvm install 16
nvm use 16

# Clear npm cache
npm cache clean --force
```

3. Missing System Dependencies:
- Verify Python version compatibility
- Check Node.js and npm versions
- Install required system packages

## Project Structure

```
├── static/
│   ├── css/
│   │   ├── src/
│   │   │   └── input.css      # Tailwind source
│   │   ├── custom.css         # Custom styles
│   │   └── tailwind.css       # Generated styles
│   ├── images/
│   │   ├── uploads/           # Uploaded images storage
│   │   └── assets/            # Static SVG assets
│   └── js/
│       └── main.js           # Frontend JavaScript
├── templates/
│   ├── admin/
│   │   └── testimonials.html
│   ├── base.html             # Base template
│   ├── about.html
│   ├── contact.html
│   ├── gallery.html
│   ├── index.html
│   ├── products.html
│   └── quote.html
├── app.py                    # Flask application
├── models.py                 # Database models
└── routes.py                # Route handlers
```

## Features

### Admin Interface
- Secure authentication system using Flask-Login
- Product management (CRUD operations)
  - Add, edit, and delete products
  - Manage product categories
  - Update product images and specifications
- Gallery project management
  - Create and edit project entries
  - Manage project images
  - Update completion dates and specifications
- Team member management
  - Add and edit team profiles
  - Update team member roles and bios
  - Manage profile photos
- Testimonial management
  - Review and approve testimonials
  - Feature selected testimonials
  - Manage client feedback
- Secure photo upload system
  - Image validation and processing
  - Secure file handling
  - Size and format restrictions
- Role-based access control
  - Admin authentication
  - Protected admin routes
  - Session management

### Product Catalog
- Categorized industrial packaging solutions
- Detailed product specifications
- ISPM 15 certification indicators
- Custom quote request system

### Quote Calculator
- Multi-step form with progress tracking
- Dynamic pricing based on:
  - Package dimensions
  - Weight specifications
  - Special requirements
  - International shipping options
- Real-time validation
- Mobile-responsive interface

### Project Gallery
- Filterable project showcase
- Categories: Type, Industry, Size
- Detailed project specifications
- ISPM 15 certification badges
- Special features highlighting

### Contact System
- Industry-specific inquiry form
- Google Maps integration
- Business hours display
- NELMA certification showcase

## Development

### Running the Development Server

1. Start the Flask development server:
```bash
python main.py
```

2. Watch Tailwind CSS changes:
```bash
npx tailwindcss -i ./static/css/src/input.css -o ./static/css/tailwind.css --watch
```

### Database Management

- Models are defined in `models.py`
- SQLAlchemy ORM for database operations
- Automatic schema creation on startup
- Sample data population for testing

### Adding New Features

1. Create new route in `routes.py`
2. Add corresponding template in `templates/`
3. Update navigation in `base.html`
4. Add necessary static assets
5. Update database models if required

## SEO Optimization

- Semantic HTML structure
- Meta tags for social sharing
- Schema.org markup for rich results
- Optimized image alt texts
- Mobile-first responsive design

## Performance Optimization

- Minified CSS with Tailwind
- Optimized SVG graphics
- Lazy loading for gallery images
- Efficient database queries
- Caching strategies implemented

## Security Features

- Flask-Login based authentication
- Role-based access control
- CSRF protection
- Secure form handling
- Input validation
- Sanitized database queries
- Secure file upload handling
- Image validation and processing
- Environment variable configuration

## License

[Add License Information]

## Contributors

[Add Contributor Information]

## Support

For support and inquiries, please contact [support@woodproductsunlimited.com](mailto:support@woodproductsunlimited.com)
