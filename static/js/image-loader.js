// Enhanced image loading performance tracking and optimization
document.addEventListener('DOMContentLoaded', function() {
    // Only track non-critical images
    const images = document.querySelectorAll('img[loading="lazy"]:not([fetchpriority="high"])');
    let loadedImages = new Set(); // Use Set to avoid duplicate counts
    const totalImages = images.length;

    function updateProgress(img) {
        if (!loadedImages.has(img)) {
            loadedImages.add(img);
            console.debug(`Loaded ${loadedImages.size}/${totalImages} lazy-loaded images`);
        }
    }

    // Intersection Observer for better lazy loading
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    // Only handle images that haven't been loaded yet
                    if (!loadedImages.has(img)) {
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                        }
                        if (img.complete) {
                            updateProgress(img);
                        } else {
                            img.addEventListener('load', () => updateProgress(img), { once: true });
                        }
                    }
                    observer.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.01
        });

        images.forEach(img => {
            if (!img.complete) {
                imageObserver.observe(img);
            } else {
                updateProgress(img);
            }
        });
    } else {
        // Fallback for browsers that don't support Intersection Observer
        images.forEach(img => {
            if (img.complete) {
                updateProgress(img);
            } else {
                img.addEventListener('load', () => updateProgress(img), { once: true });
            }
        });
    }

    // Performance metrics logging
    if ('PerformanceObserver' in window) {
        const observer = new PerformanceObserver((list) => {
            list.getEntries().forEach((entry) => {
                if (entry.initiatorType === 'img') {
                    console.debug(`Image loaded: ${entry.name}, Time: ${entry.duration}ms`);
                }
            });
        });
        observer.observe({ entryTypes: ['resource'] });
    }
});
