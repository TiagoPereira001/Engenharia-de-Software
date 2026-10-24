import { AvisoExemplo } from "../exemplo.jsx";

// Ecrã 09. Funcionalidades da release e dependências (Marta e Diogo).
export default function Release() {
  return (
    <section>
      <h1>Release 2.0</h1>
      <AvisoExemplo />
      <p>Milestone: 15 de janeiro</p>
      <table>
        <thead>
          <tr><th>Funcionalidade</th><th>Depende de</th><th>Estado</th></tr>
        </thead>
        <tbody>
          <tr><td>Exportação de relatórios em PDF</td><td>Filtros avançados</td><td>Em desenvolvimento</td></tr>
          <tr><td>Filtros avançados</td><td>-</td><td>Aprovado</td></tr>
        </tbody>
      </table>
      <p className="aviso">Aviso: Exportação de relatórios depende de Filtros avançados, que ainda não está agendada.</p>
    </section>
  );
}
