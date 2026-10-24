import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const API = process.env.API_URL || "http://127.0.0.1:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    // Em desenvolvimento o front-end e a API ficam no mesmo endereço, por isso
    // a sessão e o CSRF do Django funcionam sem configuração extra.
    // No Docker, API_URL aponta para o contentor do back-end (http://backend:8000).
    proxy: { "/api": API, "/admin": API },
  },
  test: {
    environment: "jsdom",
  },
});
