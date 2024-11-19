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

## Project Structure

```
├── static/
│   ├── css/
│   │   ├── src/
│   │   │   └── input.css      # Tailwind source
│   │   ├── custom.css         # Custom styles
│   │   └── tailwind.css       # Generated styles
│   ├── images/                # SVG assets
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

- CSRF protection
- Secure form handling
- Input validation
- Sanitized database queries
- Environment variable configuration

## License

[Add License Information]

## Contributors

[Add Contributor Information]

## Support

For support and inquiries, please contact [support@woodproductsunlimited.com](mailto:support@woodproductsunlimited.com)
