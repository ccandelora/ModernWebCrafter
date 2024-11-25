// Enhanced image loading performance tracking and optimization
document.addEventListener('DOMContentLoaded', function() {
    // Track image loading performance
    const images = document.querySelectorAll('img[loading="lazy"]');
    let loadedImages = 0;
    const totalImages = images.length;

    function updateProgress() {
        loadedImages++;
        console.debug(`Loaded ${loadedImages}/${totalImages} lazy-loaded images`);
    }

    // Intersection Observer for better lazy loading
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        if (img.complete) {
                            updateProgress();
                        } else {
                            img.addEventListener('load', updateProgress);
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
                updateProgress();
            }
        });
    } else {
        // Fallback for browsers that don't support Intersection Observer
        images.forEach(img => {
            if (img.complete) {
                updateProgress();
            } else {
                img.addEventListener('load', updateProgress);
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
