// Única porta de saída para o servidor. Os ecrãs não chamam fetch diretamente.

function lerCookie(nome) {
  const par = document.cookie.split("; ").find((c) => c.startsWith(nome + "="));
  return par ? decodeURIComponent(par.split("=")[1]) : "";
}

async function pedir(caminho, { metodo = "GET", corpo } = {}) {
  const resposta = await fetch("/api" + caminho, {
    method: metodo,
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": lerCookie("csrftoken"),
    },
    body: corpo ? JSON.stringify(corpo) : undefined,
  });
  const dados = resposta.status === 204 ? null : await resposta.json();
  if (!resposta.ok) {
    const erro = new Error("Pedido falhou");
    erro.dados = dados;
    erro.estado = resposta.status;
    throw erro;
  }
  return dados;
}

export const api = {
  eu: () => pedir("/contas/eu/"),
  entrar: (username, password) => pedir("/contas/entrar/", { metodo: "POST", corpo: { username, password } }),
  registar: (dados) => pedir("/contas/registar/", { metodo: "POST", corpo: dados }),
  sair: () => pedir("/contas/sair/", { metodo: "POST" }),
  categorias: () => pedir("/categorias/"),
  pedidos: (filtros = {}) => pedir("/pedidos/?" + new URLSearchParams(filtros)),
  pedido: (id) => pedir(`/pedidos/${id}/`),
  criarPedido: (dados) => pedir("/pedidos/", { metodo: "POST", corpo: dados }),
  parecidos: (texto) => pedir("/pedidos/parecidos/?" + new URLSearchParams({ q: texto })),
  votar: (id) => pedir(`/pedidos/${id}/voto/`, { metodo: "POST" }),
  mudarEstado: (id, para, motivo = "") => pedir(`/pedidos/${id}/estado/`, { metodo: "POST", corpo: { para, motivo } }),
};

export const ESTADOS = {
  novo: "Novo",
  em_analise: "Em análise",
  aprovado: "Aprovado",
  rejeitado: "Rejeitado",
  em_desenvolvimento: "Em desenvolvimento",
  em_revisao: "Em revisão",
  concluido: "Concluído",
};
