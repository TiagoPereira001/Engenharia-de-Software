import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Pedidos from "../paginas/Pedidos.jsx";
import { simularApi } from "./simular.js";

afterEach(cleanup);

describe("lista de pedidos", () => {
  it("mostra os pedidos com o total de votos", async () => {
    simularApi({
      "/categorias/": [],
      "/pedidos/": { results: [{ id: 1, titulo: "Exportar em PDF", categoria_nome: "Relatórios", estado_nome: "Novo", total_votos: 4 }] },
    });
    render(<MemoryRouter><Pedidos /></MemoryRouter>);
    expect(await screen.findByRole("link", { name: "Exportar em PDF" })).toBeTruthy();
    expect(screen.getByText("4")).toBeTruthy();
  });

  it("sem resultados, diz isso e deixa limpar os filtros", async () => {
    simularApi({ "/categorias/": [], "/pedidos/": { results: [] } });
    render(<MemoryRouter initialEntries={["/pedidos?q=nada"]}><Pedidos /></MemoryRouter>);
    expect(await screen.findByText(/Não há pedidos com estes filtros/)).toBeTruthy();
    expect(screen.getByRole("button", { name: "Limpar filtros" })).toBeTruthy();
  });
});
