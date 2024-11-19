/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        'wood-brown': '#8B4513',
        'wood-light': '#DEB887',
        'wood-dark': '#3E2723',
        'wood-accent': '#D7CCC8',
      },
    },
  },
  plugins: [],
}
