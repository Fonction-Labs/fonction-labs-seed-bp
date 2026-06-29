import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    fs: {
      allow: [".."],
    },
    port: 3000,
    proxy: {
      "/chatkit": {
        target: "http://localhost:8002",
        changeOrigin: true,
      },
      "/health": {
        target: "http://localhost:8002",
        changeOrigin: true,
      },
    },
  },
});
