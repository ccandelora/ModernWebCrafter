/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        // Classic Wood
        'wood-brown': '#8B4513',
        'wood-light': '#DEB887',
        'wood-dark': '#3E2723',
        'wood-accent': '#D7CCC8',
        
        // Pine Crate
        'pine-light': '#D4B48C',
        'pine-medium': '#A0522D',
        'pine-dark': '#654321',
        'pine-accent': '#E6CCB3',
        
        // Oak Crate  
        'oak-light': '#DDBF9B',
        'oak-medium': '#8B7355',
        'oak-dark': '#4A3728',
        'oak-accent': '#F2E4D5',
        
        // Cedar Crate
        'cedar-light': '#D2691E',
        'cedar-medium': '#8B4513', 
        'cedar-dark': '#3D1F00',
        'cedar-accent': '#DEB887',
      },
      
      // Theme Variables
      backgroundColor: {
        'theme-primary': 'var(--theme-primary)',
        'theme-secondary': 'var(--theme-secondary)',
        'theme-dark': 'var(--theme-dark)',
        'theme-accent': 'var(--theme-accent)',
      },
      textColor: {
        'theme-primary': 'var(--theme-primary)',
        'theme-secondary': 'var(--theme-secondary)',
        'theme-dark': 'var(--theme-dark)',
        'theme-accent': 'var(--theme-accent)',
      },
    },
  },
  plugins: [],
}
