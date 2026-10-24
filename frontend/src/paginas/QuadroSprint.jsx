import { AvisoExemplo } from "../exemplo.jsx";

const COLUNAS = {
  "Em desenvolvimento": ["Exportação de relatórios em PDF"],
  "Em revisão": ["Aviso por email quando o pedido é lido"],
  "Concluído": ["Ligação ao Slack"],
};

// Ecrã 07. Mudar de coluna muda o estado e avisa quem segue o pedido.
export default function QuadroSprint() {
  return (
    <section>
      <h1>Quadro do sprint</h1>
      <AvisoExemplo />
      <div className="colunas">
        {Object.entries(COLUNAS).map(([coluna, itens]) => (
          <div key={coluna} className="caixa">
            <strong>{coluna}</strong>
            <ul>{itens.map((i) => <li key={i}>{i}</li>)}</ul>
          </div>
        ))}
      </div>
    </section>
  );
}
