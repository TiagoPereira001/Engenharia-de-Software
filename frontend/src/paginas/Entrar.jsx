import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api.js";

// Ecrã 01. Quem se regista fica como cliente; os outros papéis atribui-os um administrador.
export default function Entrar({ aoEntrar }) {
  const [modo, setModo] = useState("entrar");
  const [dados, setDados] = useState({ username: "", email: "", password: "" });
  const [erro, setErro] = useState("");
  const navegar = useNavigate();

  const mudar = (campo) => (e) => setDados({ ...dados, [campo]: e.target.value });

  async function enviar(e) {
    e.preventDefault();
    setErro("");
    try {
      const u = modo === "entrar" ? await api.entrar(dados.username, dados.password) : await api.registar(dados);
      aoEntrar(u);
      navegar("/pedidos");
    } catch (falha) {
      setErro(falha.dados?.erro || "Não foi possível. Confirma os dados.");
    }
  }

  return (
    <section>
      <h1>{modo === "entrar" ? "Entrar" : "Criar conta"}</h1>
      <form onSubmit={enviar}>
        <label htmlFor="u">Utilizador</label>
        <input id="u" value={dados.username} onChange={mudar("username")} required />
        {modo === "registar" && (
          <>
            <label htmlFor="e">Email</label>
            <input id="e" type="email" value={dados.email} onChange={mudar("email")} />
          </>
        )}
        <label htmlFor="p">Palavra-passe</label>
        <input id="p" type="password" value={dados.password} onChange={mudar("password")} required />
        {erro && <p role="alert">{erro}</p>}
        <button type="submit">{modo === "entrar" ? "Entrar" : "Criar conta"}</button>
        <button type="button" onClick={() => setModo(modo === "entrar" ? "registar" : "entrar")}>
          {modo === "entrar" ? "Ainda não tenho conta" : "Já tenho conta"}
        </button>
      </form>
    </section>
  );
}
