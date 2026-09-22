import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Paleta dark premium
        base: "#111214",
        container: "#1A1D21",
        surface: "#23272E",
        border: "#2A2E35",
        textPrimary: "#E1E4E8",
        textSecondary: "#8B949E",
        textMuted: "#4A5058",
        userBubble: "#ECEBE4",
        accentGreen: "#4CAF7D",
        accentGreenHover: "#5DBF8E",
      },
      keyframes: {
        'fade-up': {
          '0%': { opacity: '0', transform: 'translateY(6px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
      animation: {
        'fade-up': 'fade-up 0.25s ease-out forwards',
        'fade-in': 'fade-in 0.2s ease-out forwards',
      },
      borderRadius: {
        'xl2': '20px',
      },
    },
  },
  plugins: [],
};
export default config;
