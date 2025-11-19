/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9f4',
          100: '#dcf2e3',
          200: '#bce5cc',
          300: '#8fd1a8',
          400: '#5ab37d',
          500: '#2d5016',
          600: '#1f3d0f',
          700: '#1a3210',
          800: '#162913',
          900: '#132312',
        },
        secondary: {
          50: '#f6f9f6',
          100: '#e8f0e8',
          200: '#d4e2d4',
          300: '#b3ccb3',
          400: '#8aad8a',
          500: '#4a7c59',
          600: '#3a6347',
          700: '#30503a',
          800: '#2a4232',
          900: '#25382c',
        }
      },
    },
  },
  plugins: [],
}

