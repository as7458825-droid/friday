/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'friday-blue': '#00d2ff',
        'friday-dark': '#0a0a1a',
      }
    },
  },
  plugins: [],
}
