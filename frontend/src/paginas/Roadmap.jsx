import { AvisoExemplo, RELEASES } from "../exemplo.jsx";

// Ecrã 08. Releases ao longo do tempo; a que está em risco aparece destacada (Helena).
export default function Roadmap() {
  return (
    <section>
      <h1>Roadmap</h1>
      <AvisoExemplo />
      <table>
        <thead>
          <tr><th>Release</th><th>Data</th><th>Progresso</th><th>Notas</th></tr>
        </thead>
        <tbody>
          {RELEASES.map((r) => (
            <tr key={r.nome}>
              <td>{r.nome}</td>
              <td>{r.data}</td>
              <td><div className="barra"><span style={{ width: r.progresso + "%" }} /></div> {r.progresso}%</td>
              <td>
                {r.emRisco && <div className="aviso">Em risco: faltam duas semanas para o milestone.</div>}
                {r.contrato && <div>Entrega contratual</div>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
