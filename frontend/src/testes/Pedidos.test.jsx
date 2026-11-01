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
      "/etiquetas/": ["excel"],
      "/pedidos/": { results: [{ id: 1, titulo: "Exportar em PDF", categoria_nome: "Relatórios", etiquetas: ["excel"], estado_nome: "Novo", total_votos: 4 }] },
    });
    render(<MemoryRouter><Pedidos /></MemoryRouter>);
    expect(await screen.findByRole("link", { name: "Exportar em PDF" })).toBeTruthy();
    expect(screen.getByText("4")).toBeTruthy();
    expect(await screen.findByRole("option", { name: "excel" })).toBeTruthy();
  });

  it("quem tem conta pode ver só os seus pedidos", async () => {
    simularApi({ "/categorias/": [], "/etiquetas/": [], "/pedidos/": { results: [] } });
    render(<MemoryRouter><Pedidos utilizador={{ username: "sofia", papel: "cliente" }} /></MemoryRouter>);
    expect(await screen.findByLabelText("Só os meus pedidos")).toBeTruthy();
  });

  it("sem resultados, diz isso e deixa limpar os filtros", async () => {
    simularApi({ "/categorias/": [], "/etiquetas/": [], "/pedidos/": { results: [] } });
    render(<MemoryRouter initialEntries={["/pedidos?q=nada"]}><Pedidos /></MemoryRouter>);
    expect(await screen.findByText(/Não há pedidos com estes filtros/)).toBeTruthy();
    expect(screen.getByRole("button", { name: "Limpar filtros" })).toBeTruthy();
  });
});
