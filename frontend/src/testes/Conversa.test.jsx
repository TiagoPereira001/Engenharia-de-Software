import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import Conversa from "../componentes/Conversa.jsx";
import { simularApi } from "./simular.js";

afterEach(cleanup);

const COMENTARIOS = [
  { id: 1, autor: "ricardo", texto: "Que colunas precisas?", criado_em: "2026-11-02T10:00:00Z", editado_em: null, meu: false },
  { id: 2, autor: "sofia", texto: "Total por mês.", criado_em: "2026-11-02T11:00:00Z", editado_em: "2026-11-02T11:05:00Z", meu: true },
];

function abrir(utilizador) {
  const fetchFalso = simularApi({
    "/colaboracao/pedidos/1/comentarios/": COMENTARIOS,
    "/colaboracao/pessoas/": ["diogo", "marta", "ricardo", "sofia"],
  });
  render(<Conversa pedido={1} utilizador={utilizador} />);
  return fetchFalso;
}

describe("conversa do pedido", () => {
  it("mostra autor e data, e só deixa editar ou apagar os meus (US-21)", async () => {
    abrir({ username: "sofia", papel: "cliente" });
    expect(await screen.findByText("Que colunas precisas?")).toBeTruthy();
    expect(screen.getByText(/ricardo ·/)).toBeTruthy();
    expect(screen.getByText(/· editado/)).toBeTruthy();
    expect(screen.getAllByRole("button", { name: "Editar" })).toHaveLength(1);
    expect(screen.getAllByRole("button", { name: "Apagar" })).toHaveLength(1);
  });

  it("ao escrever @ aparece a lista de pessoas (US-23)", async () => {
    abrir({ username: "diogo", papel: "programador" });
    await screen.findByText("Que colunas precisas?");
    fireEvent.change(screen.getByLabelText(/Usa @/), { target: { value: "olá @ma" } });
    fireEvent.click(await screen.findByRole("button", { name: "@marta" }));
    expect(screen.getByLabelText(/Usa @/).value).toBe("olá @marta ");
  });

  it("sem conta lê a conversa mas não comenta", async () => {
    abrir(null);
    expect(await screen.findByText("Que colunas precisas?")).toBeTruthy();
    expect(screen.getByText("Entra para comentar.")).toBeTruthy();
  });
});
