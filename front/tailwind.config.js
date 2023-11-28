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
    },
  },
  plugins: [require("@tailwindcss/aspect-ratio"), require("@tailwindcss/forms")],
};
