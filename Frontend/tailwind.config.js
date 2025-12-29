/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2563EB',
        secondary: '#10B981',
        'low-risk': '#10B981',
        'medium-risk': '#F59E0B',
        'high-risk': '#EF4444',
        background: '#F9FAFB',
        'card-bg': '#FFFFFF',
        'text-primary': '#111827',
        'text-secondary': '#6B7280',
        border: '#E5E7EB',
      },
    },
  },
  plugins: [],
}

