import { AvisoExemplo } from "../exemplo.jsx";

const PROPOSTAS = [
  ["Como gestora, quero exportar o relatório mensal em PDF, para o enviar à direção.", "do 1.º parágrafo do pedido"],
  ["Como gestora, quero escolher o período do relatório, para comparar meses.", "do 2.º parágrafo do pedido"],
];

// Ecrã 10. As histórias geradas são propostas: só entram no backlog as que o PO aceitar (Ricardo).
export default function GerarHistorias() {
  return (
    <section>
      <h1>Gerar user stories</h1>
      <AvisoExemplo />
      <p>Pedido: Exportação de relatórios em PDF</p>
      {PROPOSTAS.map(([texto, origem]) => (
        <div key={texto} className="caixa">
          <p>{texto}</p>
          <p className="nota">Saiu {origem}.</p>
          <button>Aceitar</button><button>Editar</button><button>Rejeitar</button>
        </div>
      ))}
    </section>
  );
}
