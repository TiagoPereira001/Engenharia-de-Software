import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Notificacoes from "../paginas/Notificacoes.jsx";
import { simularApi } from "./simular.js";

afterEach(cleanup);

const LISTA = {
  por_ler: 1,
  itens: [
    { id: 1, pedido: 4, tipo: "estado", texto: "«Exportar relatórios» passou a Em análise", criada_em: "2026-11-02T10:00:00Z", lida: false },
    { id: 2, pedido: 4, tipo: "mencao", texto: "diogo mencionou-te em «Exportar relatórios»", criada_em: "2026-11-01T10:00:00Z", lida: true },
  ],
};
const PREFS = { estados: true, mencoes: true, comentarios: false, email: false };

function abrir(utilizador) {
  simularApi({ "/colaboracao/notificacoes/": LISTA, "/colaboracao/preferencias/": PREFS });
  render(<MemoryRouter><Notificacoes utilizador={utilizador} /></MemoryRouter>);
}

describe("notificações", () => {
  it("avisos curtos com o pedido e o novo estado, e quantos estão por ler (Sofia)", async () => {
    abrir({ username: "sofia", papel: "cliente" });
    expect(await screen.findByRole("link", { name: "«Exportar relatórios» passou a Em análise" })).toBeTruthy();
    expect(screen.getByText("1 por ler")).toBeTruthy();
    expect(screen.getByRole("button", { name: "Marcar todas como lidas" })).toBeTruthy();
  });

  it("cada um escolhe o que recebe, também por email (US-22)", async () => {
    abrir({ username: "sofia", papel: "cliente" });
    expect((await screen.findByLabelText("também por email")).checked).toBe(false);
    expect(screen.getByLabelText("muda o estado de um pedido que sigo").checked).toBe(true);
  });

  it("sem conta, pede para entrar", () => {
    abrir(null);
    expect(screen.getByRole("link", { name: "Entra" })).toBeTruthy();
  });
});
