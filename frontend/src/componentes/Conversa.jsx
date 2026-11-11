import { useEffect, useState } from "react";
import { api } from "../api.js";

// A conversa de um pedido (ecrã 04, US-21 e US-23). @nome chama a pessoa e ela recebe uma notificação.
export default function Conversa({ pedido, utilizador }) {
  const [comentarios, setComentarios] = useState([]);
  const [texto, setTexto] = useState("");
  const [pessoas, setPessoas] = useState([]);
  const [aEditar, setAEditar] = useState(null);
  const [erro, setErro] = useState("");

  useEffect(() => {
    api.comentarios(pedido).then(setComentarios).catch(() => setErro("Não foi possível carregar a conversa."));
  }, [pedido]);

  useEffect(() => {
    if (utilizador) api.pessoas().then(setPessoas).catch(() => {});
  }, [utilizador]);

  // Sugere nomes quando a última palavra começa por @.
  const ultima = texto.split(/\s/).pop();
  const sugestoes = ultima.startsWith("@") ? pessoas.filter((p) => p.startsWith(ultima.slice(1))).slice(0, 5) : [];

  function mencionar(nome) {
    setTexto(texto.slice(0, texto.length - ultima.length) + `@${nome} `);
  }

  async function tentar(acao, falhou) {
    setErro("");
    try {
      await acao();
      setComentarios(await api.comentarios(pedido));
    } catch (falha) {
      setErro(falha.dados?.erro || falhou);
    }
  }

  async function enviar(evento) {
    evento.preventDefault();
    await tentar(async () => {
      await api.comentar(pedido, texto);
      setTexto("");
    }, "Não foi possível enviar o comentário.");
  }

  return (
    <div className="caixa">
      <strong>Conversa</strong>
      {comentarios.length === 0 && <p className="nota">Ainda não há comentários.</p>}
      <ul className="conversa">
        {comentarios.map((c) => (
          <li key={c.id}>
            <div className="nota">
              {c.autor} · {new Date(c.criado_em).toLocaleString("pt-PT")}{c.editado_em && " · editado"}
            </div>
            {aEditar?.id === c.id ? (
              <form onSubmit={(e) => { e.preventDefault(); tentar(async () => { await api.editarComentario(c.id, aEditar.texto); setAEditar(null); }, "Não foi possível editar."); }}>
                <label htmlFor={`editar-${c.id}`}>Editar comentário</label>
                <textarea id={`editar-${c.id}`} rows={2} value={aEditar.texto} onChange={(e) => setAEditar({ ...aEditar, texto: e.target.value })} />
                <button type="submit">Guardar</button>
                <button type="button" className="secundario" onClick={() => setAEditar(null)}>Cancelar</button>
              </form>
            ) : (
              <p>{c.texto}</p>
            )}
            {c.meu && aEditar?.id !== c.id && (
              <>
                <button className="secundario" onClick={() => setAEditar({ id: c.id, texto: c.texto })}>Editar</button>
                <button className="secundario" onClick={() => tentar(() => api.apagarComentario(c.id), "Não foi possível apagar.")}>Apagar</button>
              </>
            )}
          </li>
        ))}
      </ul>
      {utilizador ? (
        <form onSubmit={enviar}>
          <label htmlFor="comentario">Escreve um comentário. Usa @ para chamar alguém.</label>
          <textarea id="comentario" rows={2} value={texto} onChange={(e) => setTexto(e.target.value)} />
          {sugestoes.length > 0 && (
            <div className="sugestoes">
              {sugestoes.map((nome) => (
                <button key={nome} type="button" className="secundario" onClick={() => mencionar(nome)}>@{nome}</button>
              ))}
            </div>
          )}
          <button type="submit" disabled={!texto.trim()}>Comentar</button>
        </form>
      ) : (
        <p className="nota">Entra para comentar.</p>
      )}
      {erro && <p role="alert">{erro}</p>}
    </div>
  );
}
