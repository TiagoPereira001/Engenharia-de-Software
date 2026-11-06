# Estrutura do código

[Índice](../README.md) · [← Como correr o projeto](como-correr.md) · [Testes →](testes.md)

```
backend/
  config/            definições do Django e rotas principais
  contas/            módulo Contas: utilizador, papéis, entrar e registar
    models.py        Utilizador e Papel
    api.py           endpoints /api/contas/
  pedidos/           módulo Pedidos
    models.py        Pedido, Categoria, Etiqueta, Voto, MudancaEstado, Estado, Origem
    servicos.py      regras: criar, classificar, mudar estado (e quem pode), votar, procurar parecidos
    api.py           endpoints /api/pedidos/, /api/categorias/ e /api/etiquetas/
    tests/           testes das regras e da API
  priorizacao/       módulo Priorização
    models.py        Estimativa (impacto, esforço, lugar na ordem) e AlteracaoOrdem
    servicos.py      regras: estimar, ordenar, lista com o aviso de capacidade
    ia.py            sugestão de prioridade: Claude, ou regra local quando a IA falha
    api.py           endpoints /api/priorizacao/
    tests/           testes das regras, da IA (sem a chamar) e da API
frontend/
  src/
    App.jsx          menu e rotas (mesma ordem dos wireframes)
    api.js           única porta para o servidor
    paginas/         um ficheiro por ecrã dos wireframes
    exemplo.jsx      dados de exemplo dos ecrãs que ainda não usam a API
    testes/          testes dos ecrãs
```

## Endpoints

| Método | Caminho | O quê | Quem |
|---|---|---|---|
| GET | `/api/contas/eu/` | Quem está autenticado | Todos |
| POST | `/api/contas/registar/` | Criar conta (fica cliente) | Todos |
| POST | `/api/contas/entrar/` e `/sair/` | Entrar e sair | Todos |
| GET | `/api/categorias/` | Categorias | Todos |
| GET | `/api/etiquetas/` | Etiquetas já usadas | Todos |
| GET | `/api/pedidos/?q=&estado=&categoria=&etiqueta=&meus=1&ordem=votos` | Lista com pesquisa e filtros; `meus=1` mostra só os pedidos de quem está autenticado | Todos |
| POST | `/api/pedidos/` | Criar pedido | Autenticados |
| GET | `/api/pedidos/parecidos/?q=` | Pedidos parecidos | Todos |
| GET | `/api/pedidos/<id>/` | Detalhe com histórico e `pode_mudar_para` (os estados a que o utilizador pode levar o pedido) | Todos |
| POST | `/api/pedidos/<id>/voto/` | Votar ou retirar o voto | Autenticados |
| POST | `/api/pedidos/<id>/estado/` | Mudar o estado | Depende da passagem (tabela `QUEM_PODE` em `servicos.py`) |
| PATCH | `/api/pedidos/<id>/classificar/` | Categoria e etiquetas (US-02) | Product manager e Product Owner |
| GET | `/api/priorizacao/?ordem=&capacidade=` | Pedidos a priorizar, pela ordem pedida (`manual`, `impacto`, `esforco`, `relacao`, `votos`), com o aviso de capacidade | Todos |
| PATCH | `/api/priorizacao/<id>/estimativa/` | Impacto e esforço (US-09) | Product Owner; o esforço também o programador |
| POST | `/api/priorizacao/ordem/` | Gravar a ordem com a razão (US-06) | Product Owner |
| GET | `/api/priorizacao/historico/` | Últimas mudanças de ordem | Todos |
| GET | `/api/priorizacao/sugestao/` | Sugestão de prioridade com razão (US-08) | Product Owner |

## Ecrãs

Os 15 ecrãs do Figma existem como página. Pedidos, Novo pedido, Detalhe do pedido e Entrar já falam com a API. Os outros mostram dados de exemplo e dizem isso no topo; ligam à API no Sprint 4.

## Ver também

- [Arquitetura](../04-arquitetura/arquitetura.md)
- [Wireframes](../03-prototipo/wireframes.md)
