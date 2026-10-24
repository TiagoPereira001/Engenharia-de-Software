# Estrutura do código

[Índice](../README.md) · [← Como correr o projeto](como-correr.md) · [Testes →](testes.md)

```
backend/
  config/            definições do Django e rotas principais
  contas/            módulo Contas: utilizador, papéis, entrar e registar
    models.py        Utilizador e Papel
    permissoes.py    quem pode gerir pedidos
    api.py           endpoints /api/contas/
  pedidos/           módulo Pedidos
    models.py        Pedido, Categoria, Voto, MudancaEstado, Estado, Origem
    servicos.py      regras: criar, mudar estado, votar, procurar parecidos
    api.py           endpoints /api/pedidos/ e /api/categorias/
    tests/           testes das regras e da API
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
| GET | `/api/pedidos/?q=&estado=&categoria=&ordem=votos` | Lista com pesquisa e filtros | Todos |
| POST | `/api/pedidos/` | Criar pedido | Autenticados |
| GET | `/api/pedidos/parecidos/?q=` | Pedidos parecidos | Todos |
| GET | `/api/pedidos/<id>/` | Detalhe com histórico | Todos |
| POST | `/api/pedidos/<id>/voto/` | Votar ou retirar o voto | Autenticados |
| POST | `/api/pedidos/<id>/estado/` | Mudar o estado | Product manager e Product Owner |

## Ecrãs

Os 15 ecrãs do Figma existem como página. Pedidos, Novo pedido, Detalhe do pedido e Entrar já falam com a API. Os outros mostram dados de exemplo e dizem isso no topo; ligam à API no Sprint 4.

## Ver também

- [Arquitetura](../04-arquitetura/arquitetura.md)
- [Wireframes](../03-prototipo/wireframes.md)
