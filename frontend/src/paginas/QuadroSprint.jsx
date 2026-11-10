import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, ESTADOS } from "../api.js";

// Ecrã 07. Uma coluna por estado. Cada um só vê os botões das mudanças que o seu papel pode fazer (US-12, US-13).
export default function QuadroSprint({ utilizador }) {
  const [sprint, setSprint] = useState(null);
  const [quadro, setQuadro] = useState(null);
  const [equipas, setEquipas] = useState([]);
  const [equipa, setEquipa] = useState("");
  const [semSprint, setSemSprint] = useState(false);
  const [mensagem, setMensagem] = useState("");
  const [erro, setErro] = useState("");

  useEffect(() => {
    Promise.all([api.sprints(), api.equipas()])
      .then(([sprints, lista]) => {
        setEquipas(lista);
        const emCurso = sprints.find((s) => s.estado === "em_curso");
        emCurso ? setSprint(emCurso) : setSemSprint(true);
      })
      .catch(() => setErro("Não foi possível carregar o quadro."));
  }, []);

  useEffect(() => {
    if (sprint) api.quadro(sprint.id, equipa).then(setQuadro).catch(() => setErro("Não foi possível carregar o quadro."));
  }, [sprint, equipa, utilizador]);

  async function mudar(pedido, para) {
    setErro("");
    try {
      await api.mudarEstado(pedido, para);
      setQuadro(await api.quadro(sprint.id, equipa));
    } catch (falha) {
      setErro(falha.dados?.erro || "Não foi possível mudar o estado.");
    }
  }

  async function fechar() {
    setErro("");
    try {
      const r = await api.fecharSprint(sprint.id);
      setMensagem(`Sprint fechado. ${r.voltaram_ao_backlog} pedido(s) voltaram ao product backlog.`);
      setSprint(null);
      setQuadro(null);
      setSemSprint(true);
    } catch (falha) {
      setErro(falha.dados?.erro || "Não foi possível fechar o sprint.");
    }
  }

  if (semSprint) {
    return (
      <section>
        <h1>Quadro do sprint</h1>
        {mensagem && <p>{mensagem}</p>}
        <p>Não há nenhum sprint em curso. O Product Owner começa-o em <Link to="/sprint/planear">Planear sprint</Link>.</p>
      </section>
    );
  }
  if (!quadro) return erro ? <p role="alert">{erro}</p> : <p>A carregar...</p>;

  const total = quadro.colunas.reduce((soma, c) => soma + c.itens.length, 0);
  const concluidas = quadro.colunas.find((c) => c.estado === "concluido").itens.length;

  return (
    <section>
      <div className="cabecalho">
        <div>
          <h1>{quadro.sprint.nome}</h1>
          <p className="nota">{concluidas} de {total} funcionalidades concluídas · {quadro.sprint.pontos} de {quadro.sprint.capacidade} pontos</p>
        </div>
        <div>
          <label htmlFor="equipa">Equipa</label>
          <select id="equipa" value={equipa} onChange={(e) => setEquipa(e.target.value)}>
            <option value="">Todas</option>
            {equipas.map((e) => <option key={e.id} value={e.id}>{e.nome}</option>)}
          </select>
          {utilizador?.papel === "product_owner" && <button className="secundario" onClick={fechar}>Fechar sprint</button>}
        </div>
      </div>
      {erro && <p role="alert">{erro}</p>}
      <div className="colunas">
        {quadro.colunas.map((coluna) => (
          <div key={coluna.estado} className="caixa">
            <strong>{coluna.nome}</strong> <span className="nota">{coluna.itens.length}</span>
            <ul className="cartoes">
              {coluna.itens.map((item) => (
                <li key={item.pedido} className="cartao">
                  <Link to={`/pedidos/${item.pedido}`}>{item.titulo}</Link>
                  <div className="nota">{item.equipa?.nome || "sem equipa"}{item.esforco ? ` · ${item.esforco} pontos` : ""}</div>
                  {item.pode_mudar_para.map((para) => (
                    <button key={para} className="secundario" onClick={() => mudar(item.pedido, para)}>→ {ESTADOS[para]}</button>
                  ))}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </section>
  );
}
