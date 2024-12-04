// Theme switcher functionality
document.addEventListener('DOMContentLoaded', function() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    const savedTheme = localStorage.getItem('theme');
    const themes = ['light', 'dark', 'industrial', 'industrial-dark', 'corporate', 'executive', 'wpu'];
    
    // Function to update theme
    function updateTheme(theme) {
        // Remove all theme classes first
        document.documentElement.removeAttribute('data-theme');
        document.body.classList.remove(...themes.map(t => `theme-${t}`));
        
        // Add new theme
        document.documentElement.setAttribute('data-theme', theme);
        document.body.classList.add(`theme-${theme}`);
        
        // Update all theme switchers on the page
        const themeSwitchers = document.querySelectorAll('[data-theme-switch]');
        themeSwitchers.forEach(switcher => {
            if (switcher.tagName === 'SELECT') {
                switcher.value = theme;
            } else {
                switcher.setAttribute('data-active-theme', theme);
            }
        });
        
        // Store in localStorage
        localStorage.setItem('theme', theme);
        
        // Dispatch custom event for other components
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    }
    
    // Set initial theme
    if (savedTheme && themes.includes(savedTheme)) {
        updateTheme(savedTheme);
    } else {
        updateTheme(prefersDark.matches ? 'dark' : 'light');
    }
    
    // Listen for theme switch changes
    document.addEventListener('click', function(e) {
        const themeButton = e.target.closest('[data-theme-button]');
        if (themeButton) {
            const theme = themeButton.getAttribute('data-theme');
            if (themes.includes(theme)) {
                updateTheme(theme);
            }
        }
    });
    
    // Listen for select element changes
    document.addEventListener('change', function(e) {
        if (e.target.matches('[data-theme-switch]')) {
            const theme = e.target.value;
            if (themes.includes(theme)) {
                updateTheme(theme);
            }
        }
    });
    
    // Listen for system theme changes
    prefersDark.addEventListener('change', function(e) {
        if (!localStorage.getItem('theme')) {
            updateTheme(e.matches ? 'dark' : 'light');
        }
    });
    
    // Expose theme functions globally for programmatic access
    window.themeManager = {
        setTheme: updateTheme,
        getTheme: () => localStorage.getItem('theme') || (prefersDark.matches ? 'dark' : 'light'),
        getThemes: () => [...themes],
    };
});
