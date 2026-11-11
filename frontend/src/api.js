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
  etiquetas: () => pedir("/etiquetas/"),
  pedidos: (filtros = {}) => pedir("/pedidos/?" + new URLSearchParams(filtros)),
  pedido: (id) => pedir(`/pedidos/${id}/`),
  criarPedido: (dados) => pedir("/pedidos/", { metodo: "POST", corpo: dados }),
  parecidos: (texto) => pedir("/pedidos/parecidos/?" + new URLSearchParams({ q: texto })),
  votar: (id) => pedir(`/pedidos/${id}/voto/`, { metodo: "POST" }),
  mudarEstado: (id, para, motivo = "") => pedir(`/pedidos/${id}/estado/`, { metodo: "POST", corpo: { para, motivo } }),
  classificar: (id, dados) => pedir(`/pedidos/${id}/classificar/`, { metodo: "PATCH", corpo: dados }),
  priorizacao: (params = {}) => pedir("/priorizacao/?" + new URLSearchParams(params)),
  estimar: (id, dados) => pedir(`/priorizacao/${id}/estimativa/`, { metodo: "PATCH", corpo: dados }),
  ordenar: (dados) => pedir("/priorizacao/ordem/", { metodo: "POST", corpo: dados }),
  historicoOrdem: () => pedir("/priorizacao/historico/"),
  sugestao: () => pedir("/priorizacao/sugestao/"),
  backlog: () => pedir("/backlog/"),
  acrescentarAoBacklog: (pedido) => pedir("/backlog/", { metodo: "POST", corpo: { pedido } }),
  equipas: () => pedir("/backlog/equipas/"),
  atribuirEquipa: (pedido, equipa) => pedir(`/backlog/${pedido}/equipa/`, { metodo: "PATCH", corpo: { equipa } }),
  sprints: () => pedir("/backlog/sprints/"),
  criarSprint: (dados) => pedir("/backlog/sprints/", { metodo: "POST", corpo: dados }),
  sprint: (id) => pedir(`/backlog/sprints/${id}/`),
  porNoSprint: (id, pedido) => pedir(`/backlog/sprints/${id}/itens/`, { metodo: "POST", corpo: { pedido } }),
  tirarDoSprint: (id, pedido) => pedir(`/backlog/sprints/${id}/itens/${pedido}/`, { metodo: "DELETE" }),
  comecarSprint: (id) => pedir(`/backlog/sprints/${id}/comecar/`, { metodo: "POST" }),
  fecharSprint: (id) => pedir(`/backlog/sprints/${id}/fechar/`, { metodo: "POST" }),
  comentarios: (pedido) => pedir(`/colaboracao/pedidos/${pedido}/comentarios/`),
  comentar: (pedido, texto) => pedir(`/colaboracao/pedidos/${pedido}/comentarios/`, { metodo: "POST", corpo: { texto } }),
  editarComentario: (id, texto) => pedir(`/colaboracao/comentarios/${id}/`, { metodo: "PATCH", corpo: { texto } }),
  apagarComentario: (id) => pedir(`/colaboracao/comentarios/${id}/`, { metodo: "DELETE" }),
  pessoas: () => pedir("/colaboracao/pessoas/"),
  notificacoes: () => pedir("/colaboracao/notificacoes/"),
  marcarLidas: (ids = []) => pedir("/colaboracao/notificacoes/lidas/", { metodo: "POST", corpo: { ids } }),
  preferencias: () => pedir("/colaboracao/preferencias/"),
  guardarPreferencias: (dados) => pedir("/colaboracao/preferencias/", { metodo: "PUT", corpo: dados }),
  quadro: (id, equipa = "") => pedir(`/backlog/sprints/${id}/quadro/?` + new URLSearchParams(equipa ? { equipa } : {})),
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
