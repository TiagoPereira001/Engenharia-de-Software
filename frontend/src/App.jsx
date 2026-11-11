import { useEffect, useState } from "react";
import { Link, NavLink, Navigate, Route, Routes, useLocation } from "react-router-dom";
import { api } from "./api.js";
import Entrar from "./paginas/Entrar.jsx";
import Pedidos from "./paginas/Pedidos.jsx";
import NovoPedido from "./paginas/NovoPedido.jsx";
import DetalhePedido from "./paginas/DetalhePedido.jsx";
import Priorizacao from "./paginas/Priorizacao.jsx";
import PlanearSprint from "./paginas/PlanearSprint.jsx";
import QuadroSprint from "./paginas/QuadroSprint.jsx";
import Roadmap from "./paginas/Roadmap.jsx";
import Release from "./paginas/Release.jsx";
import GerarHistorias from "./paginas/GerarHistorias.jsx";
import Rastreabilidade from "./paginas/Rastreabilidade.jsx";
import Notificacoes from "./paginas/Notificacoes.jsx";
import EspacoEquipa from "./paginas/EspacoEquipa.jsx";
import Dashboard from "./paginas/Dashboard.jsx";
import CargaEquipas from "./paginas/CargaEquipas.jsx";

// O menu segue as áreas do enunciado, pela mesma ordem dos wireframes (Figma, Baixa Fidelidade).
export const AREAS = [
  { area: "Pedidos", ecras: [["/pedidos", "Pedidos"], ["/pedidos/novo", "Novo pedido"]] },
  { area: "Priorização", ecras: [["/priorizacao", "Priorização"]] },
  { area: "Backlog", ecras: [["/sprint/planear", "Planear sprint"], ["/sprint/quadro", "Quadro do sprint"]] },
  { area: "Roadmap", ecras: [["/roadmap", "Roadmap"], ["/roadmap/release", "Release 2.0"]] },
  { area: "Requisitos", ecras: [["/requisitos/gerar", "Gerar user stories"], ["/requisitos/rastreabilidade", "Rastreabilidade"]] },
  { area: "Colaboração", ecras: [["/notificacoes", "Notificações"], ["/equipa", "Espaço da equipa"]] },
  { area: "Dashboards", ecras: [["/dashboard", "Dashboard"], ["/dashboard/carga", "Carga das equipas"]] },
];

export default function App() {
  const [utilizador, setUtilizador] = useState(null);
  const [porLer, setPorLer] = useState(0);
  const location = useLocation();

  useEffect(() => {
    api.eu().then((r) => setUtilizador(r.autenticado ? r.utilizador : null)).catch(() => {});
  }, []);

  // O número de notificações por ler (ecrã 12) atualiza-se a cada mudança de ecrã.
  useEffect(() => {
    if (!utilizador) return setPorLer(0);
    api.notificacoes().then((r) => setPorLer(r.por_ler)).catch(() => {});
  }, [utilizador, location.pathname]);

  async function sair() {
    await api.sair();
    setUtilizador(null);
  }

  return (
    <div className="aplicacao">
      <nav className="menu">
        <strong>Pedidos e Roadmap</strong>
        {AREAS.map(({ area, ecras }) => (
          <div key={area}>
            <h2>{area}</h2>
            {ecras.map(([caminho, nome]) => (
              <NavLink key={caminho} to={caminho} end>{nome}</NavLink>
            ))}
          </div>
        ))}
        <div className="rodape">
          {utilizador ? (
            <>
              <NavLink to="/notificacoes">Notificações{porLer > 0 && <span className="contador">{porLer}</span>}</NavLink>
              <div>{utilizador.username} ({utilizador.papel})</div>
              <button onClick={sair}>Sair</button>
            </>
          ) : (
            <Link to="/entrar">Entrar</Link>
          )}
        </div>
      </nav>
      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/pedidos" replace />} />
          <Route path="/entrar" element={<Entrar aoEntrar={setUtilizador} />} />
          <Route path="/pedidos" element={<Pedidos utilizador={utilizador} />} />
          <Route path="/pedidos/novo" element={<NovoPedido utilizador={utilizador} />} />
          <Route path="/pedidos/:id" element={<DetalhePedido utilizador={utilizador} />} />
          <Route path="/priorizacao" element={<Priorizacao utilizador={utilizador} />} />
          <Route path="/sprint/planear" element={<PlanearSprint utilizador={utilizador} />} />
          <Route path="/sprint/quadro" element={<QuadroSprint utilizador={utilizador} />} />
          <Route path="/roadmap" element={<Roadmap />} />
          <Route path="/roadmap/release" element={<Release />} />
          <Route path="/requisitos/gerar" element={<GerarHistorias />} />
          <Route path="/requisitos/rastreabilidade" element={<Rastreabilidade />} />
          <Route path="/notificacoes" element={<Notificacoes utilizador={utilizador} />} />
          <Route path="/equipa" element={<EspacoEquipa />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/dashboard/carga" element={<CargaEquipas />} />
        </Routes>
      </main>
    </div>
  );
}
