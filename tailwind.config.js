/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
  ],
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        'wood-brown': 'var(--color-wood-brown)',
        'wood-light': 'var(--color-wood-light)',
        'wood-dark': 'var(--color-wood-dark)',
        'wood-accent': 'var(--color-wood-accent)',
        'theme-text': 'var(--color-text)',
        'theme-bg': 'var(--color-bg)',
        'theme-primary': 'var(--color-primary)',
        'theme-secondary': 'var(--color-secondary)',
        'industrial': {
          red: {
            DEFAULT: '#f90d0e',
            light: '#fd9e9e',
            dark: '#330101'
          },
          blue: {
            DEFAULT: '#4152e4',
            light: '#8c96ef',
            dark: '#162399'
          }
        }
      },
      transitionProperty: {
        'theme': 'background-color, border-color, color, fill, stroke',
      },
      transitionDuration: {
        '2000': '2000ms',
      },
    },
  },
  plugins: [],
}
