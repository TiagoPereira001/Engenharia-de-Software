import { AvisoExemplo, RELEASES } from "../exemplo.jsx";

const METRICAS = [
  ["Pedidos submetidos", "42"],
  ["Aprovados / rejeitados", "18 / 6"],
  ["Lead time médio", "21 dias"],
  ["Cycle time médio", "8 dias"],
];

// Ecrã 14. Números já calculados, sem relatórios à mão (Helena). Sem horas nem commits.
export default function Dashboard() {
  return (
    <section>
      <h1>Dashboard</h1>
      <AvisoExemplo />
      <div className="colunas">
        {METRICAS.map(([nome, valor]) => (
          <div key={nome} className="caixa"><div>{nome}</div><strong>{valor}</strong></div>
        ))}
      </div>
      <div className="caixa">
        <strong>Progresso das releases</strong>
        {RELEASES.map((r) => (
          <p key={r.nome}>{r.nome}: {r.progresso}% do planeado</p>
        ))}
      </div>
      <div className="caixa">
        <strong>Paradas há mais de três dias</strong>
        <ul>
          <li>Aviso por email quando o pedido é lido · Em revisão há 5 dias</li>
          <li>Filtrar por data de validade · Em análise há 4 dias</li>
        </ul>
      </div>
      <button>Exportar</button>
    </section>
  );
}
