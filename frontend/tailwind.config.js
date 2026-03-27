/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50:  '#f0faf4',
          100: '#dcf5e5',
          200: '#baeacf',
          300: '#87d9ad',
          400: '#4fbe82',
          500: '#2d9e62',
          600: '#1e7d4c',
          700: '#1a643e',
          800: '#185033',
          900: '#14422a',
        },
        green: {
          brand: '#2D7D46',
          bright: '#4CAF71',
        }
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
      },
      boxShadow: {
        card: '0 2px 12px rgba(0,0,0,0.07)',
        'card-lg': '0 4px 24px rgba(0,0,0,0.10)',
      },
    },
  },
  plugins: [],
}
