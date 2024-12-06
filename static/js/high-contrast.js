function toggleHighContrast() {
    const html = document.documentElement;
    const button = document.getElementById('high-contrast-toggle');
    const isHighContrast = html.classList.toggle('high-contrast');
    
    // Update button state
    button.setAttribute('aria-pressed', isHighContrast);
    
    // Save preference
    localStorage.setItem('highContrast', isHighContrast);
    
    // Announce change to screen readers
    const message = isHighContrast ? 'High contrast mode enabled' : 'High contrast mode disabled';
    announceToScreenReader(message);
}

function announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('class', 'sr-only');
    announcement.textContent = message;
    document.body.appendChild(announcement);
    
    // Remove after announcement
    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
}

// Initialize high contrast mode based on saved preference
document.addEventListener('DOMContentLoaded', function() {
    const savedPreference = localStorage.getItem('highContrast');
    const button = document.getElementById('high-contrast-toggle');
    
    if (savedPreference === 'true') {
        document.documentElement.classList.add('high-contrast');
        button.setAttribute('aria-pressed', 'true');
    }
});
