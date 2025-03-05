/** @type {import('tailwindcss').Config} */

const defaultTheme = require("tailwindcss/defaultTheme");

export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter var", ...defaultTheme.fontFamily.sans],
        secondary: ["Rowdies", "sans-serif"],
      },
      animation: {
        text: "slideUpDown 2.1s ease-in-out infinite",
        "fade-in": "fadeIn 0.1s ease-out",
        scale: "scaleUp 0.2s forwards",
      },

      keyframes: {
        slideUpDown: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(1.1px)" },
        },
        fadeIn: {
          "0%": { opacity: "0", transform: "translateY(-20px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        scaleUp: {
          "0%": { transform: "scale(1)" },
          "100%": { transform: "scale(1.01)" },
        },
      },
    },
  },
  plugins: [require("@tailwindcss/aspect-ratio"), require("@tailwindcss/forms"), require("@tailwindcss/postcss")],
};
