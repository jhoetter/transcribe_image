/** @type {import("tailwindcss").Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  prefix: "",
  theme: {
    extend: {
      colors: {
        border: {
          DEFAULT: "#e4e4e7",
          dark: "#27272d",
        },
        background: {
          DEFAULT: "#f4f4f5",
          dark: "#09090b",
        },
        foreground: {
          DEFAULT: "#09090b",
          dark: "#fafafa",
        },
        primary: {
          DEFAULT: "#09090b",
          foreground: "#fafafa",
          dark: "#fafafa",
          "dark-foreground": "#09090b",
        },
        secondary: {
          DEFAULT: "#f4f4f5",
          foreground: "#09090b",
          dark: "#27272d",
          "dark-foreground": "#fafafa",
        },
        muted: {
          DEFAULT: "#f4f4f5",
          foreground: "#71717a",
          dark: "#27272d",
          "dark-foreground": "#a1a1aa",
        },
        accent: {
          DEFAULT: "#f4f4f5",
          foreground: "#09090b",
          dark: "#27272d",
          "dark-foreground": "#fafafa",
        },
        destructive: {
          DEFAULT: "#ef4444",
          foreground: "#fafafa",
          dark: "#7f1d1d",
          "dark-foreground": "#fafafa",
        },
        card: {
          DEFAULT: "#ffffff",
          foreground: "#09090b",
          dark: "#18181b",
          "dark-foreground": "#fafafa",
        },
        popover: {
          DEFAULT: "#ffffff",
          foreground: "#09090b",
          dark: "#09090b",
          "dark-foreground": "#fafafa",
        },
        sidebar: {
          background: "#fafafa",
          foreground: "#3f3f46",
          dark: "#18181b",
          "dark-foreground": "#f4f4f5",
          border: "#e4e4e7",
          "dark-border": "#27272d",
        },
        chart: {
          1: "#f97316",
          2: "#22d3ee",
          3: "#22c55e",
          4: "#a855f7",
          5: "#f43f5e",
          "dark-1": "#3b82f6",
          "dark-2": "#2dd4bf",
          "dark-3": "#facc15",
          "dark-4": "#d8b4fe",
          "dark-5": "#fb7185",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      animation: {
        gradient: "gradient 3s linear infinite",
        spin: "spin 1s linear infinite",
      },
      keyframes: {
        gradient: {
          "0%, 100%": { backgroundPosition: "0% 50%" },
          "50%": { backgroundPosition: "100% 50%" },
        },
        spin: {
          from: { transform: "rotate(0deg)" },
          to: { transform: "rotate(360deg)" },
        },
      },
    },
  },
  plugins: [require("tailwindcss-animate"), require("@tailwindcss/typography")],
};
