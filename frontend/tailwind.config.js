export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          50: '#fefce8',
          100: '#fef9c3',
          200: '#fef08a',
          300: '#fde047',
          400: '#facc15',
          500: '#eab308',
          600: '#ca8a04',
          700: '#a16207',
          800: '#854d0e',
          900: '#713f12',
          950: '#422006',
        },
        accent: {
          pink: '#ec4899',
          cyan: '#06b6d4',
          amber: '#f59e0b',
          purple: '#8b5cf6',
          black: '#1a1a2e',
        }
      },
      fontFamily: {
        'grotesk': ['Space Grotesk', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
