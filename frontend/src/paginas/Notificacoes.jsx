import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api.js";

const OPCOES = [
  ["mencoes", "alguém me menciona"],
  ["estados", "muda o estado de um pedido que sigo"],
  ["comentarios", "há comentários novos em pedidos que sigo"],
  ["email", "também por email"],
];

// Ecrã 12. Avisos curtos: o pedido e o que mudou (Sofia, US-22). Cada um escolhe o que recebe.
export default function Notificacoes({ utilizador }) {
  const [dados, setDados] = useState(null);
  const [prefs, setPrefs] = useState(null);
  const [mensagem, setMensagem] = useState("");
  const [erro, setErro] = useState("");

  useEffect(() => {
    if (!utilizador) return;
    Promise.all([api.notificacoes(), api.preferencias()])
      .then(([lista, escolhas]) => {
        setDados(lista);
        setPrefs(escolhas);
      })
      .catch(() => setErro("Não foi possível carregar as notificações."));
  }, [utilizador]);

  async function marcar(ids = []) {
    try {
      setDados(await api.marcarLidas(ids));
    } catch {
      setErro("Não foi possível marcar como lidas.");
    }
  }

  async function guardar(evento) {
    evento.preventDefault();
    try {
      setPrefs(await api.guardarPreferencias(prefs));
      setMensagem("Preferências guardadas.");
    } catch {
      setErro("Não foi possível guardar as preferências.");
    }
  }

  if (!utilizador) {
    return (
      <section>
        <h1>Notificações</h1>
        <p><Link to="/entrar">Entra</Link> para veres as tuas notificações.</p>
      </section>
    );
  }
  if (!dados || !prefs) return erro ? <p role="alert">{erro}</p> : <p>A carregar...</p>;

  return (
    <section className="duas-colunas">
      <div>
        <div className="cabecalho">
          <div>
            <h1>Notificações</h1>
            <p className="nota">{dados.por_ler} por ler</p>
          </div>
          {dados.por_ler > 0 && <button className="secundario" onClick={() => marcar()}>Marcar todas como lidas</button>}
        </div>
        {dados.itens.length === 0 && <p>Ainda não tens notificações.</p>}
        <ul className="notificacoes">
          {dados.itens.map((n) => (
            <li key={n.id} className={n.lida ? "lida" : "por-ler"}>
              {n.pedido ? (
                <Link to={`/pedidos/${n.pedido}`} onClick={() => !n.lida && marcar([n.id])}>{n.texto}</Link>
              ) : (
                n.texto
              )}
              <span className="nota"> · {new Date(n.criada_em).toLocaleString("pt-PT")}</span>
            </li>
          ))}
        </ul>
        {erro && <p role="alert">{erro}</p>}
      </div>
      <aside>
        <form className="caixa" onSubmit={guardar}>
          <strong>Avisa-me quando...</strong>
          {OPCOES.map(([campo, texto]) => (
            <label key={campo} className="opcao">
              <input type="checkbox" checked={prefs[campo]} onChange={(e) => setPrefs({ ...prefs, [campo]: e.target.checked })} />
              {texto}
            </label>
          ))}
          <button type="submit">Guardar preferências</button>
          {mensagem && <p className="nota">{mensagem}</p>}
        </form>
      </aside>
    </section>
  );
}
