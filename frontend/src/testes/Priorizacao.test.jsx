import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Priorizacao from "../paginas/Priorizacao.jsx";
import { simularApi } from "./simular.js";

afterEach(cleanup);

const ESCALA = { impacto: [{ valor: 1, nome: "Baixo" }, { valor: 2, nome: "Médio" }, { valor: 3, nome: "Alto" }], esforco: [1, 2, 3, 5, 8, 13] };
const item = (id, titulo, extra = {}) => ({
  id, titulo, estado: "aprovado", estado_nome: "Aprovado", total_votos: 2, impacto: 3, esforco: 5,
  relacao: 0.6, posicao: id, fora_da_capacidade: false, ...extra,
});
const LISTA = {
  itens: [item(1, "Exportar relatórios"), item(2, "Ligação ao Slack", { esforco: 13, fora_da_capacidade: true })],
  capacidade: 15,
  aviso: "A ordem que definiste soma 18 pontos e a capacidade do sprint é 15. Os pedidos marcados já não cabem.",
  escala: ESCALA,
};
const SUGESTAO = {
  fonte: "regra local",
  ordem_sugerida: [1, 2],
  sugestoes: [
    { pedido_id: 1, titulo: "Exportar relatórios", nivel: "alta", razao: "Impacto alto." },
    { pedido_id: 2, titulo: "Ligação ao Slack", nivel: "baixa", razao: "Esforço alto." },
  ],
};

function abrir(papel) {
  const fetchFalso = simularApi({ "/priorizacao/": LISTA, "/priorizacao/sugestao/": SUGESTAO, "/priorizacao/ordem/": LISTA });
  render(<MemoryRouter><Priorizacao utilizador={papel && { username: "x", papel }} /></MemoryRouter>);
  return fetchFalso;
}

describe("priorização", () => {
  it("avisa quando a ordem passa a capacidade (Ricardo)", async () => {
    abrir("product_owner");
    expect(await screen.findByText(/a capacidade do sprint é 15/)).toBeTruthy();
  });

  it("quem não é Product Owner vê a ordem mas não a muda", async () => {
    abrir("cliente");
    expect(await screen.findByText("Exportar relatórios")).toBeTruthy();
    expect(screen.queryByRole("button", { name: /Subir/ })).toBeNull();
    expect(screen.queryByText("Porque esta ordem?")).toBeNull();
  });

  it("o programador estima o esforço, mas não o impacto", async () => {
    abrir("programador");
    expect(await screen.findByLabelText("Esforço de Exportar relatórios")).toBeTruthy();
    expect(screen.queryByLabelText("Impacto de Exportar relatórios")).toBeNull();
  });

  it("a sugestão mostra a razão e deixa manter a minha ordem (Ricardo)", async () => {
    abrir("product_owner");
    fireEvent.click(await screen.findByRole("button", { name: "Pedir sugestão" }));
    expect(await screen.findByText(/Razão: Impacto alto/)).toBeTruthy();
    expect(screen.getByText(/regra local/)).toBeTruthy();
    expect(screen.getByRole("button", { name: "Manter a minha ordem" })).toBeTruthy();
  });

  it("mudar a ordem e guardar envia a ordem nova com a razão", async () => {
    const fetchFalso = abrir("product_owner");
    fireEvent.click(await screen.findByRole("button", { name: "Descer Exportar relatórios" }));
    fireEvent.change(screen.getByLabelText(/Razão/), { target: { value: "O Slack é para o cliente principal" } });
    fireEvent.click(screen.getByRole("button", { name: "Guardar ordem" }));
    await screen.findByText("Exportar relatórios");
    const envio = fetchFalso.mock.calls.find(([url]) => url.includes("/priorizacao/ordem/"));
    expect(JSON.parse(envio[1].body)).toEqual({ ids: [2, 1], razao: "O Slack é para o cliente principal", aceitou_sugestao_ia: false });
  });
});
