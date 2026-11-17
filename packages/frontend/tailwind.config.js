/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        industrial: {
          950: '#050505', // Fondo negro puro mate
          900: '#0c0c0e', // Superficie de paneles
          850: '#141418', // Fondo de tarjetas
          800: '#1c1c22', // Fondo de inputs y selectores
          700: '#27272a', // Bordes gris acero
          600: '#3f3f46', // Bordes interactivos
          accent: '#dc2626', // Rojo rave / techno principal
          bright: '#ef4444', // Rojo brillante de alerta
          glow: 'rgba(239, 68, 68, 0.35)',
          warning: '#f59e0b', // Amarillo industrial hazard
          success: '#10b981', // Verde industrial seguro
        }
      },
      fontFamily: {
        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
      }
    },
  },
  plugins: [],
}
