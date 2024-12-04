// Theme switcher functionality
document.addEventListener('DOMContentLoaded', function() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    const savedTheme = localStorage.getItem('theme');
    const themes = ['light', 'dark', 'industrial', 'industrial-dark', 'corporate', 'executive', 'wpu'];
    
    console.log('Theme switcher initialized');
    console.log('Saved theme:', savedTheme);
    console.log('System prefers dark:', prefersDark.matches);
    
    // Function to update theme
    function updateTheme(theme) {
        console.log('Updating theme to:', theme);
        
        // Remove all theme classes first
        console.log('Removing existing theme classes and attributes');
        document.documentElement.removeAttribute('data-theme');
        const currentThemeClasses = themes.map(t => `theme-${t}`);
        document.body.classList.remove(...currentThemeClasses);
        console.log('Current body classes after removal:', document.body.className);
        
        // Add new theme
        console.log('Adding new theme:', theme);
        document.documentElement.setAttribute('data-theme', theme);
        document.body.classList.add(`theme-${theme}`);
        console.log('Updated body classes:', document.body.className);
        
        // Update all theme switchers on the page
        const themeSwitchers = document.querySelectorAll('[data-theme-switch], #theme-switch');
        console.log('Found theme switchers:', themeSwitchers.length);
        
        themeSwitchers.forEach(switcher => {
            console.log('Updating switcher:', switcher.tagName, switcher.id);
            if (switcher.tagName === 'SELECT') {
                switcher.value = theme;
            } else {
                switcher.setAttribute('data-active-theme', theme);
            }
        });
        
        // Store in localStorage
        console.log('Saving theme to localStorage:', theme);
        localStorage.setItem('theme', theme);
        
        // Dispatch custom event for other components
        console.log('Dispatching themeChanged event');
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    }
    
    // Set initial theme
    if (savedTheme && themes.includes(savedTheme)) {
        console.log('Applying saved theme:', savedTheme);
        updateTheme(savedTheme);
    } else {
        const defaultTheme = prefersDark.matches ? 'dark' : 'light';
        console.log('No saved theme, applying default:', defaultTheme);
        updateTheme(defaultTheme);
    }
    
    // Listen for theme switch changes
    document.addEventListener('click', function(e) {
        const themeButton = e.target.closest('[data-theme-button]');
        if (themeButton) {
            const theme = themeButton.getAttribute('data-theme');
            console.log('Theme button clicked:', theme);
            if (themes.includes(theme)) {
                updateTheme(theme);
            } else {
                console.warn('Invalid theme selected:', theme);
            }
        }
    });
    
    // Listen for select element changes
    document.addEventListener('change', function(e) {
        if (e.target.matches('[data-theme-switch], #theme-switch')) {
            const theme = e.target.value;
            console.log('Theme select changed:', theme);
            if (themes.includes(theme)) {
                updateTheme(theme);
            } else {
                console.warn('Invalid theme selected:', theme);
            }
        }
    });
    
    // Listen for system theme changes
    prefersDark.addEventListener('change', function(e) {
        console.log('System theme preference changed:', e.matches ? 'dark' : 'light');
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
    
    console.log('Theme switcher setup complete');
});
