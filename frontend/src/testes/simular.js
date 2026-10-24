import { vi } from "vitest";

// Substitui o fetch: cada teste diz o que a API responde a cada caminho.
export function simularApi(respostas) {
  const fetchFalso = vi.fn(async (url) => {
    const caminho = url.replace(/^\/api/, "").split("?")[0];
    const corpo = respostas[caminho];
    if (corpo === undefined) return { ok: false, status: 404, json: async () => ({}) };
    return { ok: true, status: 200, json: async () => corpo };
  });
  globalThis.fetch = fetchFalso;
  return fetchFalso;
}
