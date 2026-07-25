import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        card: "hsl(var(--card))",
        "card-foreground": "hsl(var(--card-foreground))",
        primary: {
          DEFAULT: "#6366f1",
          foreground: "#ffffff",
        },
        secondary: {
          DEFAULT: "#1e293b",
          foreground: "#f8fafc",
        },
        accent: {
          DEFAULT: "#10b981",
          foreground: "#ffffff",
        },
        muted: {
          DEFAULT: "#0f172a",
          foreground: "#94a3b8",
        },
      },
      animation: {
        "pulse-glow": "pulseGlow 2s infinite ease-in-out",
        "spin-slow": "spin 12s linear infinite",
      },
      keyframes: {
        pulseGlow: {
          "0%, 100%": { opacity: "0.8", filter: "drop-shadow(0 0 15px rgba(99, 102, 241, 0.4))" },
          "50%": { opacity: "1", filter: "drop-shadow(0 0 25px rgba(99, 102, 241, 0.8))" },
        },
      },
    },
  },
  plugins: [],
};
export default config;
