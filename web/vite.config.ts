import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from "path";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
     alias: {
       "@": path.resolve(__dirname, "./src"),
       "@components": path.resolve(__dirname, "./src/components"),
       "@pages": path.resolve(__dirname, "./src/pages"),
       "@models": path.resolve(__dirname, "./src/models"),
       "@css": path.resolve(__dirname, "./src/css"),
       "@utils": path.resolve(__dirname, "./src/utils"),
       "@data": path.resolve(__dirname, "./data"),
     },
   },
})
