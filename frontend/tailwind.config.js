/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
      },
      colors: {
        fatigue: {
          low: '#34d399',     // green-400
          medium: '#fbbf24',  // yellow-400
          high: '#fb923c',    // orange-400
          danger: '#f87171',  // red-400
        },
        slate: {
          900: '#0f172a',
          800: '#1e293b',
          700: '#334155',
        },
      },
      boxShadow: {
        card: '0 4px 12px rgba(0,0,0,0.25)',
      },
      transitionProperty: {
        'colors': 'background-color, border-color, color, fill, stroke',
      },
    },
  },
  plugins: [],
  safelist: [
    'bg-green-400',
    'bg-yellow-400',
    'bg-orange-400',
    'bg-red-500',
    'text-green-400',
    'text-yellow-400',
    'text-orange-400',
    'text-red-400',
    'bg-yellow-300',
    'text-yellow-300',
    'dark:bg-slate-900',
    'dark:text-gray-100',
    'dark:bg-slate-800',
    'dark:text-blue-400',
    'dark:border-slate-700',
    'dark:bg-slate-700',
    'dark:bg-slate-600',
    'dark:text-slate-400',
    'dark:text-slate-300',
    'dark:text-red-400',
    'dark:text-green-400',
    'dark:text-yellow-300',
    'dark:text-orange-400',
  ],
};
