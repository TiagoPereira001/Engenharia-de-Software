import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import NovoPedido from "../paginas/NovoPedido.jsx";
import { simularApi } from "./simular.js";

afterEach(cleanup);

const PARECIDOS = [
  { id: 1, titulo: "Exportação de relatórios em PDF", estado_nome: "Em análise", total_votos: 3, votei: false },
  { id: 2, titulo: "Exportar contactos", estado_nome: "Novo", total_votos: 0, votei: false },
];

function abrir(papel) {
  simularApi({ "/categorias/": [{ id: 1, nome: "Relatórios" }], "/pedidos/parecidos/": PARECIDOS });
  render(<MemoryRouter><NovoPedido utilizador={{ username: "x", papel }} /></MemoryRouter>);
}

describe("novo pedido", () => {
  it("mostra os parecidos enquanto se escreve, cada um com o seu botão de votar", async () => {
    abrir("cliente");
    fireEvent.change(screen.getByLabelText("Título"), { target: { value: "exportar relatório" } });
    const botoes = await screen.findAllByRole("button", { name: "Votar" });
    expect(botoes).toHaveLength(2);
  });

  it("não procura parecidos com menos de 4 letras", async () => {
    const fetchFalso = simularApi({ "/categorias/": [], "/pedidos/parecidos/": PARECIDOS });
    render(<MemoryRouter><NovoPedido utilizador={{ username: "x", papel: "cliente" }} /></MemoryRouter>);
    fireEvent.change(screen.getByLabelText("Título"), { target: { value: "pdf" } });
    await new Promise((r) => setTimeout(r, 400));
    expect(fetchFalso.mock.calls.some(([url]) => url.includes("parecidos"))).toBe(false);
  });

  it("o cliente não escolhe a origem, nem etiquetas", () => {
    abrir("cliente");
    expect(screen.queryByLabelText(/Origem/)).toBeNull();
    expect(screen.queryByLabelText(/Etiquetas/)).toBeNull();
  });

  it("o product manager regista a origem", () => {
    abrir("product_manager");
    expect(screen.getByLabelText(/Origem/)).toBeTruthy();
  });
});
