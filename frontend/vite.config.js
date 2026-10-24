import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    // Em desenvolvimento o front-end e a API ficam no mesmo endereço, por isso
    // a sessão e o CSRF do Django funcionam sem configuração extra.
    proxy: { "/api": "http://127.0.0.1:8000", "/admin": "http://127.0.0.1:8000" },
  },
  test: {
    environment: "jsdom",
  },
});
