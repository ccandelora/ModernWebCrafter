// Theme switcher functionality
document.addEventListener('DOMContentLoaded', function() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    const savedTheme = localStorage.getItem('theme');
    
    // Function to update theme
    function updateTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        document.body.classList.remove('theme-light', 'theme-dark');
        document.body.classList.add(`theme-${theme}`);
        
        // Update switch state
        const themeSwitch = document.getElementById('theme-switch');
        if (themeSwitch) {
            themeSwitch.checked = theme === 'dark';
        }
        
        // Update icons
        const moonIcon = document.getElementById('theme-switch-moon');
        const sunIcon = document.getElementById('theme-switch-sun');
        if (moonIcon && sunIcon) {
            moonIcon.classList.toggle('hidden', theme === 'light');
            sunIcon.classList.toggle('hidden', theme === 'dark');
        }
        
        localStorage.setItem('theme', theme);
    }
    
    // Set initial theme
    if (savedTheme) {
        updateTheme(savedTheme);
    } else {
        updateTheme(prefersDark.matches ? 'dark' : 'light');
    }
    
    // Listen for theme switch changes
    const themeSwitch = document.getElementById('theme-switch');
    themeSwitch?.addEventListener('change', function(e) {
        updateTheme(e.target.checked ? 'dark' : 'light');
    });
    
    // Listen for system theme changes
    prefersDark.addEventListener('change', function(e) {
        if (!localStorage.getItem('theme')) {
            updateTheme(e.matches ? 'dark' : 'light');
        }
    });
});
