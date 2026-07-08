import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const backendUrl = env.VITE_BACKEND_URL || "http://localhost:8002";

  return {
    plugins: [react()],
    server: {
      fs: {
        allow: [".."],
      },
      port: 3000,
      proxy: {
        "/chatkit": {
          target: backendUrl,
          changeOrigin: true,
        },
        "/health": {
          target: backendUrl,
          changeOrigin: true,
        },
      },
    },
  };
});
