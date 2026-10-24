import { AvisoExemplo, EQUIPAS } from "../exemplo.jsx";

// Ecrã 15. Carga em esforço e por tipo de trabalho; passar a capacidade gera aviso (Helena).
export default function CargaEquipas() {
  return (
    <section>
      <h1>Carga das equipas</h1>
      <AvisoExemplo />
      <table>
        <thead>
          <tr><th>Equipa</th><th>Novo</th><th>Manutenção</th><th>Bugs</th><th>Administrativo</th><th>Total / capacidade</th></tr>
        </thead>
        <tbody>
          {EQUIPAS.map((e) => {
            const total = e.novo + e.manutencao + e.bugs + e.administrativo;
            return (
              <tr key={e.nome}>
                <td>{e.nome}</td><td>{e.novo}</td><td>{e.manutencao}</td><td>{e.bugs}</td><td>{e.administrativo}</td>
                <td>
                  {total} / {e.capacidade}
                  {total > e.capacidade && <div className="aviso">Acima da capacidade</div>}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
      <p className="nota">Valores em pontos de esforço estimado.</p>
    </section>
  );
}
