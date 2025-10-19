import path from "path";
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";


// https://vitejs.dev/config/
export default defineConfig({
  server: {
    host: '0.0.0.0', // Allows external access, necessary for Docker
    port: 3000,      // Set the desired port
    allowedHosts: ['cafesansfil-b4ip.onrender.com'],
  },
  plugins: [react(), tailwindcss()],
  css: {
    modules: true,
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@components": path.resolve(__dirname, "./src/components"),
      "@data": path.resolve(__dirname, "./data"),
    },
  },
  define: {
    APP_NAME: JSON.stringify("Café sans-fil"),
    APP_VERSION: JSON.stringify(process.env.npm_package_version),
  },
});
