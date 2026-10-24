import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import App, { AREAS } from "../App.jsx";
import { simularApi } from "./simular.js";

afterEach(cleanup);

describe("menu", () => {
  it("tem os ecrãs dos wireframes, mais o Entrar", async () => {
    simularApi({ "/contas/eu/": { autenticado: false }, "/categorias/": [], "/pedidos/": { results: [] } });
    render(<MemoryRouter><App /></MemoryRouter>);
    const menu = within(screen.getByRole("navigation"));
    const ecras = AREAS.flatMap((a) => a.ecras.map(([, nome]) => nome));
    for (const nome of ecras) {
      expect(menu.getByRole("link", { name: nome })).toBeTruthy();
    }
    expect(await menu.findByRole("link", { name: "Entrar" })).toBeTruthy();
    // 13 no menu + Entrar + Detalhe do pedido (abre a partir da lista) = os 15 ecrãs do Figma
    expect(ecras.length + 2).toBe(15);
  });
});
