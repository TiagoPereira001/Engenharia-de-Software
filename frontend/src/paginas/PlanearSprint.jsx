import { AvisoExemplo, BACKLOG } from "../exemplo.jsx";

// Ecrã 06. Só entra no sprint o que tem estimativa e critérios de aceitação (Ricardo).
export default function PlanearSprint() {
  return (
    <section>
      <h1>Planear sprint</h1>
      <AvisoExemplo />
      <div className="duas-colunas">
        <div className="caixa">
          <strong>Product backlog</strong>
          <ul>
            {BACKLOG.map((p) => {
              const pronto = p.estimado && p.criterios;
              return (
                <li key={p.titulo}>
                  {p.titulo}{" "}
                  {pronto ? (
                    <button>Pôr no sprint</button>
                  ) : (
                    <span>(não entra: {!p.estimado ? "falta estimativa" : "faltam critérios de aceitação"})</span>
                  )}
                </li>
              );
            })}
          </ul>
        </div>
        <div className="caixa">
          <strong>Sprint 4</strong>
          <p>Arrasta para aqui os itens do backlog.</p>
          <p>Capacidade: 7 de 15 pontos</p>
          <div className="barra"><span style={{ width: "47%" }} /></div>
        </div>
      </div>
    </section>
  );
}
