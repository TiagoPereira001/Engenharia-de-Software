import { AvisoExemplo } from "../exemplo.jsx";

// Ecrã 11. Do pedido chega-se ao código, e do pull request volta-se ao pedido.
export default function Rastreabilidade() {
  return (
    <section>
      <h1>Rastreabilidade</h1>
      <AvisoExemplo />
      <table>
        <thead>
          <tr><th>Pedido</th><th>User story</th><th>Implementação</th></tr>
        </thead>
        <tbody>
          <tr><td>Exportação de relatórios em PDF</td><td>Exportar o relatório mensal em PDF</td><td>Pull request #12</td></tr>
          <tr><td>Exportação de relatórios em PDF</td><td>Escolher o período do relatório</td><td>Ainda sem implementação</td></tr>
        </tbody>
      </table>
    </section>
  );
}
