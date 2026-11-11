import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api, ESTADOS } from "../api.js";
import Conversa from "../componentes/Conversa.jsx";

// Ecrã 04. Estado, etiquetas, votos (só o total) e histórico.
// Os botões de mudar estado vêm do servidor (pode_mudar_para): o ecrã não repete as regras.
export default function DetalhePedido({ utilizador }) {
  const { id } = useParams();
  const [pedido, setPedido] = useState(null);
  const [motivo, setMotivo] = useState("");
  const [etiquetas, setEtiquetas] = useState("");
  const [erro, setErro] = useState("");

  useEffect(() => {
    api
      .pedido(id)
      .then((p) => {
        setPedido(p);
        setEtiquetas(p.etiquetas.join(", "));
      })
      .catch(() => setErro("Pedido não encontrado."));
  }, [id, utilizador]);

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

  async function guardarEtiquetas(evento) {
    evento.preventDefault();
    setErro("");
    try {
      const atualizado = await api.classificar(id, { etiquetas: etiquetas.split(",") });
      setPedido(atualizado);
      setEtiquetas(atualizado.etiquetas.join(", "));
    } catch (falha) {
      setErro(falha.dados?.erro || "Não foi possível guardar as etiquetas.");
    }
  }

  if (erro && !pedido) return <p role="alert">{erro}</p>;
  if (!pedido) return <p>A carregar...</p>;

  const gere = utilizador && ["product_manager", "product_owner"].includes(utilizador.papel);
  const seguintes = pedido.pode_mudar_para || [];

  return (
    <section className="duas-colunas">
      <div>
        <h1>{pedido.titulo}</h1>
        <p>{pedido.categoria_nome} · {pedido.estado_nome} · pedido por {pedido.autor}</p>
        <p>{pedido.etiquetas.map((e) => <span key={e} className="etiqueta">{e}</span>)}</p>
        <p>{pedido.descricao}</p>
        <p>
          {pedido.total_votos} votos{" "}
          {utilizador && <button onClick={votar}>{pedido.votei ? "Retirar voto" : "Votar"}</button>}
        </p>
        <Conversa pedido={pedido.id} utilizador={utilizador} />
        {gere && (
          <form className="caixa" onSubmit={guardarEtiquetas}>
            <label htmlFor="etiquetas">Etiquetas (separadas por vírgulas)</label>
            <input id="etiquetas" value={etiquetas} onChange={(e) => setEtiquetas(e.target.value)} />
            <button type="submit">Guardar etiquetas</button>
          </form>
        )}
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
        {seguintes.length > 0 && (
          <div className="caixa">
            <strong>Mudar estado</strong>
            {seguintes.includes("rejeitado") && (
              <>
                <label htmlFor="motivo">Motivo (obrigatório para rejeitar)</label>
                <textarea id="motivo" rows={2} value={motivo} onChange={(e) => setMotivo(e.target.value)} />
              </>
            )}
            {seguintes.map((para) => (
              <button key={para} onClick={() => mudar(para)}>{ESTADOS[para]}</button>
            ))}
          </div>
        )}
        {erro && <p role="alert">{erro}</p>}
      </aside>
    </section>
  );
}
