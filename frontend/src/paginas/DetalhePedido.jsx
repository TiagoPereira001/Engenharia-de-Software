import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api, ESTADOS } from "../api.js";

// Mesmas transições do servidor e do diagrama de estados.
const PROXIMOS = {
  novo: ["em_analise"],
  em_analise: ["aprovado", "rejeitado"],
  aprovado: ["em_desenvolvimento"],
  em_desenvolvimento: ["em_revisao"],
  em_revisao: ["em_desenvolvimento", "concluido"],
};

// Ecrã 04. Estado, votos (só o total) e histórico. Comentários e menções ficam para o Sprint 4.
export default function DetalhePedido({ utilizador }) {
  const { id } = useParams();
  const [pedido, setPedido] = useState(null);
  const [motivo, setMotivo] = useState("");
  const [erro, setErro] = useState("");

  useEffect(() => {
    api.pedido(id).then(setPedido).catch(() => setErro("Pedido não encontrado."));
  }, [id]);

  async function votar() {
    const r = await api.votar(id);
    setPedido({ ...pedido, total_votos: r.total_votos, votei: r.votei });
  }

  async function mudar(para) {
    setErro("");
    try {
      setPedido(await api.mudarEstado(id, para, motivo));
      setMotivo("");
    } catch (falha) {
      setErro(falha.dados?.erro || falha.dados?.detail || "Não foi possível mudar o estado.");
    }
  }

  if (erro && !pedido) return <p role="alert">{erro}</p>;
  if (!pedido) return <p>A carregar...</p>;

  const gere = utilizador && ["product_manager", "product_owner"].includes(utilizador.papel);

  return (
    <section className="duas-colunas">
      <div>
        <h1>{pedido.titulo}</h1>
        <p>{pedido.categoria_nome} · {pedido.estado_nome} · pedido por {pedido.autor}</p>
        <p>{pedido.descricao}</p>
        <p>
          {pedido.total_votos} votos{" "}
          {utilizador && <button onClick={votar}>{pedido.votei ? "Retirar voto" : "Votar"}</button>}
        </p>
        <div className="caixa">
          <strong>Comentários</strong>
          <p className="nota">Comentários, menções e versões entram no Sprint 4.</p>
        </div>
      </div>
      <aside>
        <div className="caixa">
          <strong>Histórico</strong>
          <ol>
            {pedido.historico.map((h, i) => (
              <li key={i}>
                {ESTADOS[h.para]} · {h.autor} · {new Date(h.quando).toLocaleString("pt-PT")}
                {h.motivo && <div>Motivo: {h.motivo}</div>}
              </li>
            ))}
          </ol>
        </div>
        {gere && (PROXIMOS[pedido.estado] || []).length > 0 && (
          <div className="caixa">
            <strong>Mudar estado</strong>
            <label htmlFor="motivo">Motivo (obrigatório para rejeitar)</label>
            <textarea id="motivo" rows={2} value={motivo} onChange={(e) => setMotivo(e.target.value)} />
            {PROXIMOS[pedido.estado].map((para) => (
              <button key={para} onClick={() => mudar(para)}>{ESTADOS[para]}</button>
            ))}
            {erro && <p role="alert">{erro}</p>}
          </div>
        )}
      </aside>
    </section>
  );
}
