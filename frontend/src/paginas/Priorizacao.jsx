import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api.js";

const ORDENS = [
  ["manual", "Ordem do Product Owner"],
  ["relacao", "Impacto por ponto de esforço"],
  ["impacto", "Impacto"],
  ["esforco", "Esforço (menor primeiro)"],
  ["votos", "Votos"],
];

function mover(lista, de, para) {
  const nova = [...lista];
  const [item] = nova.splice(de, 1);
  nova.splice(para, 0, item);
  return nova;
}

// Ecrã 05. A ordem é do Product Owner; a IA só sugere, e diz sempre porquê (Ricardo, US-06, US-08, US-09).
export default function Priorizacao({ utilizador }) {
  const [ordem, setOrdem] = useState("manual");
  const [dados, setDados] = useState(null);
  const [itens, setItens] = useState([]);
  const [mudou, setMudou] = useState(false);
  const [razao, setRazao] = useState("");
  const [sugestao, setSugestao] = useState(null);
  const [historico, setHistorico] = useState(null);
  const [erro, setErro] = useState("");

  const papel = utilizador?.papel;
  const eProductOwner = papel === "product_owner";
  const estimaEsforco = eProductOwner || papel === "programador";

  function mostrar(resposta) {
    setDados(resposta);
    setItens(resposta.itens);
    setMudou(false);
  }

  useEffect(() => {
    api.priorizacao({ ordem }).then(mostrar).catch(() => setErro("Não foi possível carregar a priorização."));
  }, [ordem]);

  async function tentar(acao, mensagem) {
    setErro("");
    try {
      await acao();
    } catch (falha) {
      setErro(falha.dados?.erro || mensagem);
    }
  }

  const estimar = (id, campo, valor) =>
    tentar(async () => mostrar(await api.estimar(id, { [campo]: Number(valor) })), "Não foi possível guardar a estimativa.");

  const guardar = (aceitouIa = false) =>
    tentar(async () => {
      const ids = aceitouIa ? sugestao.ordem_sugerida : itens.map((i) => i.id);
      const texto = aceitouIa && !razao ? "Aceitei a sugestão da IA." : razao;
      mostrar(await api.ordenar({ ids, razao: texto, aceitou_sugestao_ia: aceitouIa }));
      setRazao("");
      setSugestao(null);
      if (historico) setHistorico(await api.historicoOrdem());
    }, "Não foi possível guardar a ordem.");

  const pedirSugestao = () => tentar(async () => setSugestao(await api.sugestao()), "Não foi possível pedir a sugestão.");

  const verHistorico = () =>
    tentar(async () => setHistorico(historico ? null : await api.historicoOrdem()), "Não foi possível ver o histórico.");

  if (!dados) return erro ? <p role="alert">{erro}</p> : <p>A carregar...</p>;

  const nivelDe = Object.fromEntries((sugestao?.sugestoes || []).map((s) => [s.pedido_id, s.nivel]));
  const podeMover = eProductOwner && ordem === "manual";

  return (
    <section className="duas-colunas">
      <div>
        <div className="cabecalho">
          <h1>Priorização</h1>
          <button className="secundario" onClick={verHistorico}>{historico ? "Esconder histórico" : "Ver histórico"}</button>
        </div>
        <p className="nota">
          {eProductOwner
            ? "Usa as setas para mudar a ordem. Cada mudança fica registada com data, autor e razão."
            : "A ordem é do Product Owner. Aqui vês a ordem atual."}
        </p>
        <label htmlFor="ordem">Ver por</label>
        <select id="ordem" value={ordem} onChange={(e) => setOrdem(e.target.value)}>
          {ORDENS.map(([valor, nome]) => <option key={valor} value={valor}>{nome}</option>)}
        </select>

        {itens.length === 0 ? (
          <p>Não há pedidos em análise nem aprovados para priorizar.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>#</th><th>Pedido</th><th>Votos</th><th>Impacto</th><th>Esforço</th>
                {sugestao && <th>A IA sugere</th>}
                {podeMover && <th>Mover</th>}
              </tr>
            </thead>
            <tbody>
              {itens.map((p, i) => (
                <tr key={p.id} className={p.fora_da_capacidade ? "fora" : undefined}>
                  <td>{p.posicao ?? "–"}</td>
                  <td><Link to={`/pedidos/${p.id}`}>{p.titulo}</Link> <span className="nota">{p.estado_nome}</span></td>
                  <td>{p.total_votos}</td>
                  <td>
                    {eProductOwner ? (
                      <select aria-label={`Impacto de ${p.titulo}`} value={p.impacto ?? ""} onChange={(e) => estimar(p.id, "impacto", e.target.value)}>
                        <option value="" disabled>por estimar</option>
                        {dados.escala.impacto.map((n) => <option key={n.valor} value={n.valor}>{n.nome}</option>)}
                      </select>
                    ) : (
                      dados.escala.impacto.find((n) => n.valor === p.impacto)?.nome ?? "por estimar"
                    )}
                  </td>
                  <td>
                    {estimaEsforco ? (
                      <select aria-label={`Esforço de ${p.titulo}`} value={p.esforco ?? ""} onChange={(e) => estimar(p.id, "esforco", e.target.value)}>
                        <option value="" disabled>sem estimativa</option>
                        {dados.escala.esforco.map((n) => <option key={n} value={n}>{n} pontos</option>)}
                      </select>
                    ) : (
                      p.esforco ? `${p.esforco} pontos` : "sem estimativa"
                    )}
                  </td>
                  {sugestao && <td><span className="post-it">{nivelDe[p.id]}</span></td>}
                  {podeMover && (
                    <td>
                      <button aria-label={`Subir ${p.titulo}`} disabled={i === 0} onClick={() => { setItens(mover(itens, i, i - 1)); setMudou(true); }}>↑</button>
                      <button aria-label={`Descer ${p.titulo}`} disabled={i === itens.length - 1} onClick={() => { setItens(mover(itens, i, i + 1)); setMudou(true); }}>↓</button>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        )}
        {dados.aviso && <p className="aviso">{dados.aviso}</p>}
        {erro && <p role="alert">{erro}</p>}

        {historico && (
          <div className="caixa">
            <strong>Histórico da ordem</strong>
            {historico.length === 0 && <p className="nota">A ordem ainda não foi mudada.</p>}
            <ol>
              {historico.map((h) => (
                <li key={h.id}>
                  {new Date(h.quando).toLocaleString("pt-PT")} · {h.autor}
                  {h.aceitou_sugestao_ia && " · aceitou a sugestão da IA"}
                  {h.razao && <div>{h.razao}</div>}
                </li>
              ))}
            </ol>
          </div>
        )}
      </div>

      {eProductOwner && (
        <aside>
          <div className="caixa">
            <strong>Porque esta ordem?</strong>
            <label htmlFor="razao">Razão (fica no histórico)</label>
            <textarea id="razao" rows={3} value={razao} onChange={(e) => setRazao(e.target.value)} />
            <button onClick={() => guardar(false)} disabled={!mudou && !razao}>Guardar ordem</button>
          </div>
          <div className="caixa">
            <strong>Sugestão da IA</strong>
            {!sugestao ? (
              <button className="secundario" onClick={pedirSugestao}>Pedir sugestão</button>
            ) : (
              <>
                {sugestao.fonte !== "ia" && (
                  <p className="nota">O serviço de IA não está disponível. Esta sugestão foi feita com a regra local (votos, impacto e esforço).</p>
                )}
                <ol>
                  {sugestao.sugestoes.map((s) => (
                    <li key={s.pedido_id}>{s.titulo} ({s.nivel}). Razão: {s.razao}</li>
                  ))}
                </ol>
                <button onClick={() => guardar(true)}>Aceitar as sugestões</button>
                <button className="secundario" onClick={() => setSugestao(null)}>Manter a minha ordem</button>
              </>
            )}
            <p className="nota">A IA só sugere. Nada muda sem o Product Owner aceitar.</p>
          </div>
        </aside>
      )}
    </section>
  );
}
