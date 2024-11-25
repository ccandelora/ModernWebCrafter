document.addEventListener('DOMContentLoaded', function() {
    const heroImage = document.querySelector('.hero-image');
    if (heroImage) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * 0.5;
            heroImage.style.transform = `translate3d(0px, ${rate}px, 0px)`;
        });
    }
});
