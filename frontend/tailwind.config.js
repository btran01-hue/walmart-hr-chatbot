/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Walmart brand colors
        'walmart-blue': '#0071ce',
        'walmart-yellow': '#ffc220',
        'walmart-dark': '#041e42',
      },
    },
  },
  plugins: [],
}
