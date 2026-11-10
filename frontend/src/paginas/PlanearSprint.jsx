import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api.js";

const VAZIO = { nome: "", objetivo: "", inicio: "", fim: "", capacidade: 10 };

function Cartao({ item, children }) {
  return (
    <li className="cartao">
      <Link to={`/pedidos/${item.pedido}`}>{item.titulo}</Link>
      <div className="nota">
        {item.esforco ? `${item.esforco} pontos` : item.motivo || "sem estimativa"} · {item.equipa?.nome || item.estado_nome}
      </div>
      {children}
    </li>
  );
}

// Ecrã 06. O product backlog segue a ordem do Product Owner; só entra no sprint o que tem estimativa (US-10, US-11).
export default function PlanearSprint({ utilizador }) {
  const [backlog, setBacklog] = useState([]);
  const [aprovados, setAprovados] = useState([]);
  const [sprint, setSprint] = useState(null);
  const [semSprint, setSemSprint] = useState(false);
  const [novo, setNovo] = useState(VAZIO);
  const [mensagem, setMensagem] = useState("");
  const [erro, setErro] = useState("");

  const eProductOwner = utilizador?.papel === "product_owner";

  async function carregar() {
    const [lista, sprints, pedidos] = await Promise.all([api.backlog(), api.sprints(), api.pedidos({ estado: "aprovado" })]);
    const planeado = sprints.find((s) => s.estado === "planeado") || sprints.find((s) => s.estado === "em_curso");
    const doSprint = planeado ? await api.sprint(planeado.id) : null;
    const dentro = new Set([...lista.itens, ...(doSprint?.itens || [])].map((i) => i.pedido));
    setBacklog(lista.itens);
    setSprint(doSprint);
    setSemSprint(!planeado);
    setAprovados(pedidos.results.filter((p) => !dentro.has(p.id)));
  }

  useEffect(() => {
    carregar().catch(() => setErro("Não foi possível carregar o backlog."));
  }, []);

  async function tentar(acao, falhou) {
    setErro("");
    setMensagem("");
    try {
      await acao();
      await carregar();
    } catch (falha) {
      setErro(falha.dados?.erro || falhou);
    }
  }

  async function criar(evento) {
    evento.preventDefault();
    await tentar(async () => {
      await api.criarSprint({ ...novo, capacidade: Number(novo.capacidade) });
      setNovo(VAZIO);
    }, "Não foi possível criar o sprint. Confirma as datas e o objetivo.");
  }

  const mudarNovo = (campo) => (e) => setNovo({ ...novo, [campo]: e.target.value });
  const percentagem = sprint ? Math.min(100, Math.round((sprint.pontos / sprint.capacidade) * 100)) : 0;

  return (
    <section>
      <div className="cabecalho">
        <div>
          <h1>{sprint ? `Planear o ${sprint.nome}` : "Planear sprint"}</h1>
          {sprint && (
            <p className="nota">
              {new Date(sprint.inicio).toLocaleDateString("pt-PT")} a {new Date(sprint.fim).toLocaleDateString("pt-PT")} · objetivo: {sprint.objetivo}
            </p>
          )}
        </div>
        {eProductOwner && sprint?.estado === "planeado" && (
          <button onClick={() => tentar(() => api.comecarSprint(sprint.id), "Não foi possível começar o sprint.")}>Começar sprint</button>
        )}
      </div>
      {erro && <p role="alert">{erro}</p>}
      {mensagem && <p>{mensagem}</p>}

      <div className="duas-colunas">
        <div className="caixa">
          <strong>Product backlog</strong> <span className="nota">{backlog.length}</span>
          {backlog.length === 0 && <p className="nota">O backlog está vazio. Acrescenta pedidos aprovados.</p>}
          <ul className="cartoes">
            {backlog.map((item) => (
              <Cartao key={item.pedido} item={item}>
                {eProductOwner && sprint && item.pronto && (
                  <button onClick={() => tentar(() => api.porNoSprint(sprint.id, item.pedido), "Não foi possível pôr no sprint.")}>
                    Pôr no sprint
                  </button>
                )}
              </Cartao>
            ))}
          </ul>
          {eProductOwner && aprovados.length > 0 && (
            <>
              <strong>Aprovados fora do backlog</strong>
              <ul>
                {aprovados.map((p) => (
                  <li key={p.id}>
                    {p.titulo}{" "}
                    <button className="secundario" onClick={() => tentar(() => api.acrescentarAoBacklog(p.id), "Não foi possível acrescentar.")}>
                      Acrescentar ao backlog
                    </button>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>

        <div className="caixa">
          {sprint ? (
            <>
              <strong>{sprint.nome}</strong> <span className="nota">{sprint.itens.length} · {sprint.estado_nome}</span>
              <ul className="cartoes">
                {sprint.itens.map((item) => (
                  <Cartao key={item.pedido} item={item}>
                    {eProductOwner && (
                      <button className="secundario" onClick={() => tentar(() => api.tirarDoSprint(sprint.id, item.pedido), "Não foi possível tirar.")}>
                        Tirar do sprint
                      </button>
                    )}
                  </Cartao>
                ))}
              </ul>
              <p>Capacidade</p>
              <div className="barra" role="progressbar" aria-valuenow={sprint.pontos} aria-valuemax={sprint.capacidade}>
                <span style={{ width: `${percentagem}%` }} />
              </div>
              <p>{sprint.pontos} de {sprint.capacidade} pontos usados</p>
              {sprint.aviso && <p className="aviso">{sprint.aviso}</p>}
            </>
          ) : semSprint && eProductOwner ? (
            <form onSubmit={criar}>
              <strong>Novo sprint</strong>
              <label htmlFor="nome">Nome</label>
              <input id="nome" value={novo.nome} onChange={mudarNovo("nome")} required />
              <label htmlFor="objetivo">Objetivo</label>
              <input id="objetivo" value={novo.objetivo} onChange={mudarNovo("objetivo")} required />
              <label htmlFor="inicio">Início</label>
              <input id="inicio" type="date" value={novo.inicio} onChange={mudarNovo("inicio")} required />
              <label htmlFor="fim">Fim</label>
              <input id="fim" type="date" value={novo.fim} onChange={mudarNovo("fim")} required />
              <label htmlFor="capacidade">Capacidade (pontos)</label>
              <input id="capacidade" type="number" min="1" value={novo.capacidade} onChange={mudarNovo("capacidade")} required />
              <button type="submit">Criar sprint</button>
            </form>
          ) : (
            <p className="nota">Ainda não há um sprint a planear. O Product Owner cria-o aqui.</p>
          )}
        </div>
      </div>
    </section>
  );
}
