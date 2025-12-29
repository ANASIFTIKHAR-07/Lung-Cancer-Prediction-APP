/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Enhanced medical-themed color palette
        primary: {
          DEFAULT: '#1E40AF',      // Deeper, more trustworthy blue
          light: '#3B82F6',        // Lighter blue for accents
          dark: '#1E3A8A',         // Darker blue for hover states
        },
        secondary: {
          DEFAULT: '#059669',      // Professional green
          light: '#10B981',
        },
        'low-risk': {
          DEFAULT: '#059669',      // Professional green
          light: '#D1FAE5',        // Light green for backgrounds
        },
        'medium-risk': {
          DEFAULT: '#D97706',      // Softer orange
          light: '#FEF3C7',        // Light orange for backgrounds
        },
        'high-risk': {
          DEFAULT: '#DC2626',      // Professional red
          light: '#FEE2E2',        // Light red for backgrounds
        },
        background: '#F8FAFC',     // Softer background
        'card-bg': '#FFFFFF',
        'text-primary': '#0F172A',   // Deeper, more readable
        'text-secondary': '#64748B', // Softer secondary text
        border: '#E2E8F0',          // Softer borders
        accent: '#6366F1',          // Purple accent for special elements
      },
      boxShadow: {
        'soft': '0 2px 8px rgba(0, 0, 0, 0.04)',
        'medium': '0 4px 16px rgba(0, 0, 0, 0.08)',
        'large': '0 8px 32px rgba(0, 0, 0, 0.12)',
        'glow': '0 0 20px rgba(30, 64, 175, 0.15)',
      },
      backgroundImage: {
        'gradient-medical': 'linear-gradient(135deg, #1E40AF 0%, #3B82F6 50%, #60A5FA 100%)',
        'gradient-soft': 'linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%)',
      },
    },
  },
  plugins: [],
}

