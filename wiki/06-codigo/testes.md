# Testes

[Índice](../README.md) · [← Estrutura do código](estrutura.md) · [Git e pull requests →](git.md)

## Correr

Com Docker (ver [como correr](como-correr.md)):

```bash
docker compose exec backend python manage.py test
docker compose exec frontend npm test
```

Sem Docker:

```bash
cd backend && .venv/bin/python manage.py test
cd frontend && npm test
```

No Docker os testes do back-end correm em PostgreSQL; sem Docker e no GitHub Actions correm em SQLite. Passam nos dois.

O GitHub Actions corre os dois em cada pull request e em cada push para a `main` (`.github/workflows/ci.yml`).

## Qualidade do código

No back-end o GitHub Actions corre também:

- **ruff**, que verifica o estilo, a ordem dos imports e erros comuns (as regras estão em `backend/pyproject.toml`);
- **coverage**, que mede que parte do código os testes percorrem. Se a cobertura descer dos 90 %, o pull request fica vermelho.

Para correr o mesmo no teu computador, sem Docker:

```bash
cd backend
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/ruff check .
.venv/bin/coverage run manage.py test
.venv/bin/coverage report
```

## O que já está testado

**Back-end (41 testes):**

- um pedido nasce Novo e fica no histórico;
- o cliente não escolhe a origem; o product manager sim;
- as mudanças de estado seguem o diagrama e as impossíveis são recusadas;
- cada papel só faz a sua parte do diagrama: o product manager faz a triagem, o programador leva até à revisão e só o Product Owner aceita (`QUEM_PODE`);
- etiquetas: ficam em minúsculas e sem repetidos, filtram a lista, e só o product manager e o Product Owner as mudam (US-02);
- "os meus pedidos" mostra só os pedidos de quem está autenticado (US-01);
- rejeitar exige motivo;
- um voto por pessoa (também na base de dados) e votar outra vez retira o voto;
- pedidos parecidos: encontra "exportação" ao escrever "exportar", ignora textos curtos e pedidos rejeitados;
- API: criar precisa de login, título curto é recusado, pesquisa e filtros juntam-se, os votos mostram só o total, o cliente não muda o estado;
- contas: quem se regista fica cliente, a palavra-passe fica com hash, o erro de entrada não diz o que falhou;
- dados de exemplo: um utilizador por papel, pedidos com histórico e votos, a palavra-passe é o nome mais 123, há um admin, e correr duas vezes não duplica;
- origem do front-end: a API aceita os POST vindos de `localhost:5173` (o proxy do Vite, também no Docker) e recusa os de outra origem.

**Front-end (27 testes):**

- o menu tem os ecrãs dos wireframes;
- Novo pedido mostra os parecidos com um botão de votar em cada um e não procura com menos de 4 letras;
- o cliente não vê Origem nem etiquetas; o product manager vê Origem;
- a lista mostra o total de votos e as etiquetas e, sem resultados, deixa limpar os filtros; quem tem conta pode ver só os seus pedidos;
- no detalhe, os botões de mudar estado são os que o servidor manda, e só quem gere pedidos edita as etiquetas;
- os 11 ecrãs com dados de exemplo abrem e avisam disso;
- o que as personas pediram está nos ecrãs: aviso de capacidade e razão da IA (Ricardo), itens sem estimativa ou critérios marcados (Ricardo), release em risco e entrega contratual, tarefas paradas e carga por tipo (Helena).

## Regra

Cada cartão de código traz testes novos. Um pull request com testes a falhar não entra na `main`.

## Ver também

- [Requisitos não funcionais](../02-requisitos/requisitos-nao-funcionais.md)
- [Git e pull requests](git.md)
