/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
    "./static/css/src/input.css"
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
          'primary': 'var(--industrial-primary)',
          'primary-light': 'var(--industrial-primary-light)',
          'primary-dark': 'var(--industrial-primary-dark)',
          'secondary': 'var(--industrial-secondary)',
          'secondary-light': 'var(--industrial-secondary-light)',
          'secondary-dark': 'var(--industrial-secondary-dark)',
          red: {
            DEFAULT: 'var(--industrial-primary, #db0c0c)',
            light: 'var(--industrial-primary-light, #fd9e9e)',
            dark: 'var(--industrial-primary-dark, #330101)'
          },
          blue: {
            DEFAULT: 'var(--industrial-secondary, #0c1edb)',
            light: 'var(--industrial-secondary-light, #8c96ef)',
            dark: 'var(--industrial-secondary-dark, #162399)'
          }
        },
        'industrial-dark': {
          primary: 'var(--industrial-primary, #0519C4)',
          'primary-light': 'var(--industrial-primary-light, #fd9e9e)',
          'primary-dark': 'var(--industrial-primary-dark, #DD0B0D)',
          secondary: 'var(--industrial-secondary, #DD0B0D)',
          'secondary-light': 'var(--industrial-secondary-light, #9A989C)',
          'secondary-dark': 'var(--industrial-secondary-dark, #3D12AB)',
          background: '#000814',
          text: '#E8E1DE',
          gray: '#9A9B9C'
        },
        'corporate': {
          'primary': 'var(--corporate-primary, #0519C4)',
          'primary-light': 'var(--corporate-primary-light, #4051B5)',
          'primary-dark': 'var(--corporate-primary-dark, #2D3748)',
          'secondary': 'var(--corporate-secondary, #DD0B0D)',
          'secondary-light': 'var(--corporate-secondary-light, #F5F7FA)',
          'secondary-dark': 'var(--corporate-secondary-dark, #B91C1C)',
        },
        'wpu': {
          'primary': 'var(--wpu-primary, #0F19BA)',
          'primary-light': 'var(--wpu-primary-light, #3D44C9)',
          'primary-dark': 'var(--wpu-primary-dark, #0A1187)',
          'secondary': 'var(--wpu-secondary, #D80F14)',
          'secondary-light': 'var(--wpu-secondary-light, #E63E42)',
          'secondary-dark': 'var(--wpu-secondary-dark, #B00C10)',
          'gray': 'var(--wpu-gray, #A5A3A8)',
          'gray-light': 'var(--wpu-gray-light, #D4D3D5)',
          'gray-dark': 'var(--wpu-gray-dark, #6B696E)',
        }
      },
      transitionProperty: {
        'theme': 'background-color, border-color, color, fill, stroke',
      },
      transitionDuration: {
        '2000': '2000ms',
      },
      boxShadow: {
        'industrial': '0 4px 6px -1px var(--industrial-primary)',
        'industrial-blue': '0 4px 6px -1px var(--industrial-secondary)',
      },
      opacity: {
        '20': '0.2',
      }
    },
  },
  safelist: [
    'hover:shadow-industrial-blue',
    {
      pattern: /shadow-(industrial|industrial-blue)\/\d+/,
      variants: ['hover']
    }
  ],
  plugins: [],
}
