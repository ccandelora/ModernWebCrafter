// Theme switcher functionality
document.addEventListener('DOMContentLoaded', function() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    const savedTheme = localStorage.getItem('theme');
    const themes = ['light', 'dark', 'industrial'];
    
    // Function to update theme
    function updateTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        document.body.classList.remove('theme-light', 'theme-dark', 'theme-industrial');
        document.body.classList.add(`theme-${theme}`);
        
        // Update select element
        const themeSwitch = document.getElementById('theme-switch');
        if (themeSwitch) {
            themeSwitch.value = theme;
        }
        
        localStorage.setItem('theme', theme);
    }
    
    // Set initial theme
    if (savedTheme && themes.includes(savedTheme)) {
        updateTheme(savedTheme);
    } else {
        updateTheme(prefersDark.matches ? 'dark' : 'light');
    }
    
    // Listen for theme switch changes
    const themeSwitch = document.getElementById('theme-switch');
    themeSwitch?.addEventListener('change', function(e) {
        updateTheme(e.target.value);
    });
    
    // Listen for system theme changes
    prefersDark.addEventListener('change', function(e) {
        if (!localStorage.getItem('theme')) {
            updateTheme(e.matches ? 'dark' : 'light');
        }
    });
});
