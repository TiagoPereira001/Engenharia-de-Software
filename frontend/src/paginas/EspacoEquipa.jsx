import { AvisoExemplo } from "../exemplo.jsx";

// Ecrã 13. Cada equipa vê só o seu trabalho: membros, funcionalidades e pedidos.
export default function EspacoEquipa() {
  return (
    <section>
      <h1>Espaço da equipa</h1>
      <AvisoExemplo />
      <div className="duas-colunas">
        <div className="caixa">
          <strong>Em curso</strong>
          <ul>
            <li>Exportação de relatórios em PDF · Diogo · Em desenvolvimento</li>
            <li>Aviso por email quando o pedido é lido · Ana · Em revisão</li>
          </ul>
        </div>
        <div className="caixa">
          <strong>Membros</strong>
          <ul><li>Diogo</li><li>Ana</li><li>Bruno</li></ul>
        </div>
      </div>
    </section>
  );
}
