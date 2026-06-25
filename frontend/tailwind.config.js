/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#10a37f',
        secondary: '#565869',
        dark: '#0d0d0d',
        light: '#f7f7f8',
      },
    },
  },
  darkMode: 'class',
  plugins: [],
}
