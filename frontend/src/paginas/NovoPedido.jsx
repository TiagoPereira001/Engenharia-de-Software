import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api.js";

const PAPEIS_QUE_REGISTAM_ORIGEM = ["product_manager", "product_owner"];

// Ecrã 03. Título, descrição e uma só categoria (Sofia). Os parecidos aparecem enquanto
// se escreve o título, cada um com o seu botão de votar (US-05).
export default function NovoPedido({ utilizador }) {
  const [dados, setDados] = useState({ titulo: "", descricao: "", categoria: "", origem: "sistema" });
  const [categorias, setCategorias] = useState([]);
  const [parecidos, setParecidos] = useState([]);
  const [erros, setErros] = useState({});
  const navegar = useNavigate();

  useEffect(() => {
    api.categorias().then(setCategorias).catch(() => {});
  }, []);

  useEffect(() => {
    if (dados.titulo.trim().length < 4) {
      setParecidos([]);
      return;
    }
    // Espera que a pessoa pare de escrever antes de perguntar ao servidor.
    const espera = setTimeout(() => {
      api.parecidos(dados.titulo).then(setParecidos).catch(() => setParecidos([]));
    }, 300);
    return () => clearTimeout(espera);
  }, [dados.titulo]);

  const mudar = (campo) => (e) => setDados({ ...dados, [campo]: e.target.value });

  async function votar(id) {
    const r = await api.votar(id);
    setParecidos(parecidos.map((p) => (p.id === id ? { ...p, total_votos: r.total_votos, votei: r.votei } : p)));
  }

  async function submeter(e) {
    e.preventDefault();
    try {
      const pedido = await api.criarPedido(dados);
      navegar(`/pedidos/${pedido.id}`);
    } catch (falha) {
      setErros(falha.dados || { geral: "Não foi possível submeter." });
    }
  }

  if (!utilizador) {
    return <p>Para submeter um pedido tens de <Link to="/entrar">entrar</Link>.</p>;
  }

  return (
    <section className="duas-colunas">
      <form onSubmit={submeter}>
        <h1>Novo pedido</h1>
        <label htmlFor="titulo">Título</label>
        <input id="titulo" value={dados.titulo} onChange={mudar("titulo")} required />
        {erros.titulo && <p role="alert">{erros.titulo}</p>}
        <label htmlFor="descricao">Descrição</label>
        <textarea id="descricao" rows={5} value={dados.descricao} onChange={mudar("descricao")} required />
        <label htmlFor="categoria">Categoria</label>
        <select id="categoria" value={dados.categoria} onChange={mudar("categoria")} required>
          <option value="">Escolhe uma</option>
          {categorias.map((c) => (
            <option key={c.id} value={c.id}>{c.nome}</option>
          ))}
        </select>
        {PAPEIS_QUE_REGISTAM_ORIGEM.includes(utilizador.papel) && (
          <>
            <label htmlFor="origem">Origem (quando registas em nome de alguém)</label>
            <select id="origem" value={dados.origem} onChange={mudar("origem")}>
              <option value="sistema">Sistema</option>
              <option value="email">Email</option>
              <option value="reuniao">Reunião</option>
              <option value="chat">Chat</option>
            </select>
          </>
        )}
        {erros.geral && <p role="alert">{erros.geral}</p>}
        <div>
          <button type="submit">Submeter</button>
          <Link to="/pedidos">Cancelar</Link>
        </div>
      </form>

      {parecidos.length > 0 && (
        <aside className="caixa" aria-label="Pedidos parecidos">
          <p>Já existem pedidos parecidos. Se for o mesmo, vota em vez de criar outro.</p>
          <ul>
            {parecidos.map((p) => (
              <li key={p.id}>
                <Link to={`/pedidos/${p.id}`}>{p.titulo}</Link> ({p.estado_nome}, {p.total_votos} votos){" "}
                <button type="button" onClick={() => votar(p.id)}>{p.votei ? "Retirar voto" : "Votar"}</button>
              </li>
            ))}
          </ul>
        </aside>
      )}
    </section>
  );
}
