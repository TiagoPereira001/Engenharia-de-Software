import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { api, ESTADOS } from "../api.js";

// Ecrã 02. Pesquisa e filtros juntos (US-04). Os filtros ficam no endereço, para se poder partilhar.
export default function Pedidos() {
  const [params, setParams] = useSearchParams();
  const [pedidos, setPedidos] = useState(null);
  const [categorias, setCategorias] = useState([]);
  const [erro, setErro] = useState("");

  useEffect(() => {
    api.categorias().then(setCategorias).catch(() => {});
  }, []);

  useEffect(() => {
    api
      .pedidos(Object.fromEntries(params))
      .then((r) => setPedidos(r.results))
      .catch(() => setErro("Não foi possível carregar os pedidos."));
  }, [params]);

  function filtrar(campo, valor) {
    const novo = new URLSearchParams(params);
    valor ? novo.set(campo, valor) : novo.delete(campo);
    setParams(novo);
  }

  return (
    <section>
      <h1>Pedidos</h1>
      <p>
        <Link to="/pedidos/novo">Novo pedido</Link>
      </p>
      <div>
        <label htmlFor="q">Pesquisar</label>
        <input id="q" defaultValue={params.get("q") || ""} onKeyDown={(e) => e.key === "Enter" && filtrar("q", e.target.value)} />
        <label htmlFor="estado">Estado</label>
        <select id="estado" value={params.get("estado") || ""} onChange={(e) => filtrar("estado", e.target.value)}>
          <option value="">Todos</option>
          {Object.entries(ESTADOS).map(([v, n]) => (
            <option key={v} value={v}>{n}</option>
          ))}
        </select>
        <label htmlFor="categoria">Categoria</label>
        <select id="categoria" value={params.get("categoria") || ""} onChange={(e) => filtrar("categoria", e.target.value)}>
          <option value="">Todas</option>
          {categorias.map((c) => (
            <option key={c.id} value={c.id}>{c.nome}</option>
          ))}
        </select>
        <label htmlFor="ordem">Ordenar</label>
        <select id="ordem" value={params.get("ordem") || ""} onChange={(e) => filtrar("ordem", e.target.value)}>
          <option value="">Mais recentes</option>
          <option value="votos">Mais votados</option>
        </select>
      </div>

      {erro && <p role="alert">{erro}</p>}
      {pedidos && pedidos.length === 0 && (
        <p>
          Não há pedidos com estes filtros. <button onClick={() => setParams({})}>Limpar filtros</button>
        </p>
      )}
      {pedidos && pedidos.length > 0 && (
        <table>
          <thead>
            <tr><th>Pedido</th><th>Categoria</th><th>Estado</th><th>Votos</th></tr>
          </thead>
          <tbody>
            {pedidos.map((p) => (
              <tr key={p.id}>
                <td><Link to={`/pedidos/${p.id}`}>{p.titulo}</Link></td>
                <td>{p.categoria_nome}</td>
                <td>{p.estado_nome}</td>
                <td>{p.total_votos}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
