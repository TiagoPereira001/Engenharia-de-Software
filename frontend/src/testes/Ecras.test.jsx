import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Priorizacao from "../paginas/Priorizacao.jsx";
import PlanearSprint from "../paginas/PlanearSprint.jsx";
import QuadroSprint from "../paginas/QuadroSprint.jsx";
import Roadmap from "../paginas/Roadmap.jsx";
import Release from "../paginas/Release.jsx";
import GerarHistorias from "../paginas/GerarHistorias.jsx";
import Rastreabilidade from "../paginas/Rastreabilidade.jsx";
import Notificacoes from "../paginas/Notificacoes.jsx";
import EspacoEquipa from "../paginas/EspacoEquipa.jsx";
import Dashboard from "../paginas/Dashboard.jsx";
import CargaEquipas from "../paginas/CargaEquipas.jsx";

afterEach(cleanup);

const abrir = (Ecra) => render(<MemoryRouter><Ecra /></MemoryRouter>);

describe("ecrãs com dados de exemplo", () => {
  const ECRAS = [
    [Priorizacao, "Priorização"], [PlanearSprint, "Planear sprint"], [QuadroSprint, "Quadro do sprint"],
    [Roadmap, "Roadmap"], [Release, "Release 2.0"], [GerarHistorias, "Gerar user stories"],
    [Rastreabilidade, "Rastreabilidade"], [Notificacoes, "Notificações"], [EspacoEquipa, "Espaço da equipa"],
    [Dashboard, "Dashboard"], [CargaEquipas, "Carga das equipas"],
  ];

  it.each(ECRAS)("%#: abre e avisa que os dados são de exemplo", (Ecra, titulo) => {
    abrir(Ecra);
    expect(screen.getByRole("heading", { name: titulo })).toBeTruthy();
    expect(screen.getByText(/dados de exemplo/)).toBeTruthy();
  });
});

describe("o que as personas pediram", () => {
  it("priorização: avisa quando a ordem passa a capacidade e mostra a razão da IA (Ricardo)", () => {
    abrir(Priorizacao);
    expect(screen.getByText(/a capacidade é/)).toBeTruthy();
    expect(screen.getAllByText(/Razão:/).length).toBeGreaterThan(0);
    expect(screen.getByRole("button", { name: "Manter a minha ordem" })).toBeTruthy();
  });

  it("planear sprint: sem estimativa ou sem critérios não entra (Ricardo)", () => {
    abrir(PlanearSprint);
    expect(screen.getByText(/falta estimativa/)).toBeTruthy();
    expect(screen.getByText(/faltam critérios de aceitação/)).toBeTruthy();
  });

  it("roadmap: a release em risco aparece destacada (Helena)", () => {
    abrir(Roadmap);
    expect(screen.getByText(/Em risco/)).toBeTruthy();
    expect(screen.getByText("Entrega contratual")).toBeTruthy();
  });

  it("dashboard: mostra as tarefas paradas há mais de três dias (Helena)", () => {
    abrir(Dashboard);
    expect(screen.getByText("Paradas há mais de três dias")).toBeTruthy();
  });

  it("carga: separa por tipo de trabalho e avisa acima da capacidade (Helena)", () => {
    abrir(CargaEquipas);
    for (const tipo of ["Novo", "Manutenção", "Bugs", "Administrativo"]) {
      expect(screen.getByRole("columnheader", { name: tipo })).toBeTruthy();
    }
    expect(screen.getByText("Acima da capacidade")).toBeTruthy();
  });
});
