/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        warm: {
          50: '#FAF9F5',
          100: '#F8F6F0',
          200: '#F1EFE6',
        },
        spider: {
          500: '#EF4444',
          600: '#DC2626',
          700: '#B91C1C',
        }
      }
    },
  },
  plugins: [],
}
