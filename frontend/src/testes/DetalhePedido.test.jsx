import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import DetalhePedido from "../paginas/DetalhePedido.jsx";
import { simularApi } from "./simular.js";

afterEach(cleanup);

const PEDIDO = {
  id: 1, titulo: "Exportar em PDF", descricao: "Para a direção.", categoria_nome: "Relatórios",
  estado: "em_analise", estado_nome: "Em análise", autor: "sofia", total_votos: 3, votei: false,
  etiquetas: ["relatórios"], historico: [], pode_mudar_para: ["aprovado", "rejeitado"],
};

function abrir(utilizador, pedido = PEDIDO) {
  simularApi({ "/pedidos/1/": pedido });
  render(
    <MemoryRouter initialEntries={["/pedidos/1"]}>
      <Routes><Route path="/pedidos/:id" element={<DetalhePedido utilizador={utilizador} />} /></Routes>
    </MemoryRouter>
  );
}

describe("detalhe do pedido", () => {
  it("os botões de estado são os que o servidor diz", async () => {
    abrir({ username: "marta", papel: "product_manager" });
    expect(await screen.findByRole("button", { name: "Aprovado" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "Rejeitado" })).toBeTruthy();
    expect(screen.getByLabelText(/Motivo/)).toBeTruthy();
  });

  it("sem estados possíveis não mostra a caixa de mudar estado", async () => {
    abrir({ username: "sofia", papel: "cliente" }, { ...PEDIDO, pode_mudar_para: [] });
    expect(await screen.findByText("relatórios")).toBeTruthy();
    expect(screen.queryByText("Mudar estado")).toBeNull();
    expect(screen.queryByLabelText(/Etiquetas/)).toBeNull();
  });

  it("o product manager edita as etiquetas", async () => {
    abrir({ username: "marta", papel: "product_manager" });
    const campo = await screen.findByLabelText(/Etiquetas/);
    expect(campo.value).toBe("relatórios");
  });
});
