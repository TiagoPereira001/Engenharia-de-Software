import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import QuadroSprint from "../paginas/QuadroSprint.jsx";
import { simularApi } from "./simular.js";

afterEach(cleanup);

const SPRINT = { id: 7, nome: "Sprint 4", estado: "em_curso", pontos: 5, capacidade: 10 };
const cartao = (pedido, titulo, pode) => ({ pedido, titulo, esforco: 2, equipa: { id: 1, nome: "Equipa A" }, pode_mudar_para: pode });
const QUADRO = {
  sprint: SPRINT,
  colunas: [
    { estado: "aprovado", nome: "Aprovado", itens: [cartao(1, "Aviso por email", ["em_desenvolvimento"])] },
    { estado: "em_desenvolvimento", nome: "Em desenvolvimento", itens: [] },
    { estado: "em_revisao", nome: "Em revisão", itens: [] },
    { estado: "concluido", nome: "Concluído", itens: [cartao(2, "Votar", [])] },
  ],
};

function abrir(papel, sprints = [SPRINT]) {
  simularApi({ "/backlog/sprints/": sprints, "/backlog/equipas/": [{ id: 1, nome: "Equipa A" }], "/backlog/sprints/7/quadro/": QUADRO });
  render(<MemoryRouter><QuadroSprint utilizador={{ username: "x", papel }} /></MemoryRouter>);
}

describe("quadro do sprint", () => {
  it("uma coluna por estado, com o progresso no topo", async () => {
    abrir("programador");
    expect(await screen.findByText("1 de 2 funcionalidades concluídas · 5 de 10 pontos")).toBeTruthy();
    for (const coluna of ["Aprovado", "Em desenvolvimento", "Em revisão", "Concluído"]) {
      expect(screen.getByText(coluna, { selector: "strong" })).toBeTruthy();
    }
  });

  it("os botões são só as mudanças que o servidor deixa fazer", async () => {
    abrir("programador");
    expect(await screen.findByRole("button", { name: "→ Em desenvolvimento" })).toBeTruthy();
    expect(screen.queryByRole("button", { name: "Fechar sprint" })).toBeNull();
  });

  it("filtra por equipa e o Product Owner pode fechar o sprint", async () => {
    abrir("product_owner");
    expect(await screen.findByRole("option", { name: "Equipa A" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "Fechar sprint" })).toBeTruthy();
  });

  it("sem sprint em curso, explica onde se começa", async () => {
    abrir("product_owner", []);
    expect(await screen.findByRole("link", { name: "Planear sprint" })).toBeTruthy();
  });
});
