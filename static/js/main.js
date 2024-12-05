document.addEventListener('DOMContentLoaded', function() {
    // Loading overlay management
    const loadingOverlay = document.getElementById('loadingOverlay');
    
    function showLoading() {
        if (loadingOverlay) {
            loadingOverlay.classList.add('active');
        }
    }
    
    function hideLoading() {
        if (loadingOverlay) {
            loadingOverlay.classList.remove('active');
        }
    }

    // Handle all form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            // Skip for logout forms
            if (form.action && form.action.includes('logout')) {
                return;
            }
            
            // Show loading overlay
            showLoading();
        });
    });

    // Product filtering
    const categoryFilters = document.querySelectorAll('.category-filter');
    categoryFilters.forEach(filter => {
        filter.addEventListener('click', function(e) {
            e.preventDefault();
            showLoading();
            const category = this.dataset.category;
            window.location.href = `/products?category=${category}`;
        });
    });

    // Form validation
    const validationForms = document.querySelectorAll('.needs-validation');
    validationForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                hideLoading();
            }
            form.classList.add('was-validated');
        });
    });

    // Image gallery
    const productImages = document.querySelectorAll('.product-gallery img');
    productImages.forEach(img => {
        img.addEventListener('click', function() {
            const modal = new bootstrap.Modal(document.getElementById('imageModal'));
            const modalImg = document.getElementById('modalImage');
            modalImg.src = this.src;
            modal.show();
        });
    });

    // Handle AJAX requests loading state
    const originalFetch = window.fetch;
    window.fetch = function() {
        showLoading();
        return originalFetch.apply(this, arguments)
            .finally(() => {
                hideLoading();
            });
    };

    // Handle browser back/forward
    window.addEventListener('pageshow', function(event) {
        if (event.persisted) {
            hideLoading();
        }
    });

    // Hide loading on initial page load
    hideLoading();
});
