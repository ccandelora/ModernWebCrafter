// Enhanced image loading with blur placeholders
document.addEventListener('DOMContentLoaded', function() {
    // Style injection for blur transition
    const style = document.createElement('style');
    style.textContent = `
        .lazy-image-wrapper {
            position: relative;
            overflow: hidden;
            background-color: #f0f0f0;
        }
        .lazy-image {
            opacity: 0;
            transition: opacity 0.3s ease-in-out, filter 0.3s ease-in-out;
            filter: blur(20px);
            will-change: opacity, filter;
        }
        .lazy-image.loaded {
            opacity: 1;
            filter: blur(0);
        }
        .lazy-placeholder {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: #f0f0f0;
            background-size: cover;
            background-position: center;
            filter: blur(10px);
            transform: scale(1.1);
        }
    `;
    document.head.appendChild(style);

    // Only track non-critical images
    const images = document.querySelectorAll('img[loading="lazy"]:not([fetchpriority="high"])');
    let loadedImages = new Set();
    const totalImages = images.length;

    function wrapImage(img) {
        // Skip if already wrapped
        if (img.parentElement.classList.contains('lazy-image-wrapper')) return;

        const wrapper = document.createElement('div');
        wrapper.className = 'lazy-image-wrapper';
        wrapper.style.paddingBottom = '75%'; // 4:3 aspect ratio by default

        // Create blur placeholder
        const placeholder = document.createElement('div');
        placeholder.className = 'lazy-placeholder';
        if (img.dataset.placeholder) {
            placeholder.style.backgroundImage = `url(${img.dataset.placeholder})`;
        }

        // Setup image
        img.className = 'lazy-image ' + img.className;
        img.style.position = 'absolute';
        img.style.top = '0';
        img.style.left = '0';
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = 'cover';

        // Wrap image
        img.parentNode.insertBefore(wrapper, img);
        wrapper.appendChild(placeholder);
        wrapper.appendChild(img);

        // Update aspect ratio if image is loaded
        if (img.complete && img.naturalWidth) {
            const ratio = (img.naturalHeight / img.naturalWidth) * 100;
            wrapper.style.paddingBottom = ratio + '%';
        }
    }

    function updateProgress(img) {
        if (!loadedImages.has(img)) {
            loadedImages.add(img);
            img.classList.add('loaded');
            console.debug(`Loaded ${loadedImages.size}/${totalImages} lazy-loaded images`);

            // Update aspect ratio
            if (img.naturalWidth) {
                const wrapper = img.closest('.lazy-image-wrapper');
                if (wrapper) {
                    const ratio = (img.naturalHeight / img.naturalWidth) * 100;
                    wrapper.style.paddingBottom = ratio + '%';
                }
            }
        }
    }

    // Wrap all lazy images
    images.forEach(wrapImage);

    // Intersection Observer for better lazy loading
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
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
