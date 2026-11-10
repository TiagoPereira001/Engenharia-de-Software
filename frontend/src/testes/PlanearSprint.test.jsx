import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import PlanearSprint from "../paginas/PlanearSprint.jsx";
import { simularApi } from "./simular.js";

afterEach(cleanup);

const item = (pedido, titulo, extra = {}) => ({
  pedido, titulo, estado: "aprovado", estado_nome: "Aprovado", esforco: 3, equipa: null,
  pronto: true, motivo: "", pode_mudar_para: [], ...extra,
});
const SPRINT = {
  id: 7, nome: "Sprint 4", objetivo: "Priorizar e planear", inicio: "2026-11-09", fim: "2026-11-20",
  capacidade: 10, estado: "planeado", estado_nome: "Planeado", pontos: 12,
  aviso: "O sprint tem 12 pontos e a capacidade é 10.", itens: [item(3, "Aviso por email", { esforco: 12 })],
};

function abrir(papel, respostas = {}) {
  simularApi({
    "/backlog/": { itens: [item(1, "Ligação ao Slack"), item(2, "Lista mais rápida", { esforco: null, pronto: false, motivo: "sem estimativa: não pode entrar" })] },
    "/backlog/sprints/": [SPRINT],
    "/backlog/sprints/7/": SPRINT,
    "/pedidos/": { results: [{ id: 9, titulo: "Exportar PDF" }] },
    ...respostas,
  });
  render(<MemoryRouter><PlanearSprint utilizador={{ username: "x", papel }} /></MemoryRouter>);
}

describe("planear sprint", () => {
  it("sem estimativa, o item diz porque não entra (Ricardo)", async () => {
    abrir("product_owner");
    expect(await screen.findByText(/sem estimativa: não pode entrar/)).toBeTruthy();
    expect(screen.getAllByRole("button", { name: "Pôr no sprint" })).toHaveLength(1);
  });

  it("mostra a capacidade usada e o aviso quando passa", async () => {
    abrir("product_owner");
    expect(await screen.findByText("12 de 10 pontos usados")).toBeTruthy();
    expect(screen.getByText(/capacidade é 10/)).toBeTruthy();
    expect(screen.getByRole("button", { name: "Começar sprint" })).toBeTruthy();
  });

  it("deixa acrescentar ao backlog os aprovados que ainda lá não estão", async () => {
    abrir("product_owner");
    expect(await screen.findByRole("button", { name: "Acrescentar ao backlog" })).toBeTruthy();
  });

  it("quem não é Product Owner vê o plano mas não mexe", async () => {
    abrir("programador");
    expect(await screen.findByText("Ligação ao Slack")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "Pôr no sprint" })).toBeNull();
    expect(screen.queryByRole("button", { name: "Começar sprint" })).toBeNull();
  });

  it("sem sprint, o Product Owner pode criar um com datas e objetivo", async () => {
    abrir("product_owner", { "/backlog/sprints/": [] });
    expect(await screen.findByLabelText("Objetivo")).toBeTruthy();
    expect(screen.getByLabelText("Capacidade (pontos)")).toBeTruthy();
  });
});
