import { AvisoExemplo, BACKLOG } from "../exemplo.jsx";

const CAPACIDADE = 15;

// Ecrã 05. A ordem é do Product Owner; a IA só sugere, e diz sempre porquê (Ricardo).
export default function Priorizacao() {
  const esforcoTotal = BACKLOG.reduce((soma, p) => soma + (p.esforco || 0), 0);
  return (
    <section className="duas-colunas">
      <div>
        <h1>Priorização</h1>
        <AvisoExemplo />
        <table>
          <thead>
            <tr><th>#</th><th>Pedido</th><th>Votos</th><th>Impacto</th><th>Esforço</th></tr>
          </thead>
          <tbody>
            {BACKLOG.map((p, i) => (
              <tr key={p.titulo}>
                <td>{i + 1}</td><td>{p.titulo}</td><td>{p.votos}</td><td>{p.impacto}</td><td>{p.esforco ?? "sem estimativa"}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {esforcoTotal > CAPACIDADE && (
          <p className="aviso">Aviso: esta ordem põe {esforcoTotal} pontos no sprint e a capacidade é {CAPACIDADE}.</p>
        )}
      </div>
      <aside className="caixa">
        <strong>Sugestão da IA</strong>
        <ol>
          <li>Aviso por email quando o pedido é lido. Razão: esforço baixo e é o pedido com mais votos.</li>
          <li>Exportação de relatórios em PDF. Razão: impacto alto num cliente importante.</li>
        </ol>
        <button>Aceitar</button>
        <button>Manter a minha ordem</button>
        <p className="nota">Se a IA não responder, a priorização manual continua a funcionar.</p>
      </aside>
    </section>
  );
}
