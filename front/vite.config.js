import path from "path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  css: {
    modules: true,
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@data": path.resolve(__dirname, "./data"),
    },
  },
  define: {
    APP_NAME: JSON.stringify("Café sans-fil"),
    APP_VERSION: JSON.stringify(process.env.npm_package_version),
  },
});
