# AGENTS.md

Regras para quem trabalha neste repositório, seja uma pessoa da equipa ou um agente de IA (Claude Code, Copilot, Codex...). A equipa usa ferramentas de IA para programar, como o enunciado pede, e este ficheiro diz-lhes como trabalhar aqui.

## Antes de começar

1. Lê o [estado atual](wiki/currentstate.md): sprint em curso, o que está feito e o que falta.
2. Abre o cartão do Jira da tarefa. O trabalho só começa a partir de um cartão.
3. Se a tarefa for de código, lê [como correr](wiki/06-codigo/como-correr.md) e a [estrutura do código](wiki/06-codigo/estrutura.md).

## O projeto em duas linhas

Sistema de gestão de pedidos de funcionalidades e roadmap (o produto do enunciado de Engenharia de Software, UBI 2026/27). Back-end Django REST Framework em `backend/`, front-end React em `frontend/`, documentação em `wiki/`.

## Comandos

```bash
# tudo de uma vez (Docker)
docker compose up --build

# back-end
cd backend && .venv/bin/python manage.py test
cd backend && .venv/bin/python manage.py runserver

# front-end
cd frontend && npm test
cd frontend && npm run dev
```

## Regras

- **Português de Portugal** no código visível ao utilizador, nos nomes do domínio (Pedido, Voto, MudancaEstado), nos commits e na documentação.
- **Os mesmos nomes em todo o lado.** Os estados de um pedido são os da US-12: Novo, Em análise, Aprovado, Rejeitado, Em desenvolvimento, Em revisão, Concluído. Se mudares um nome, muda-o no código, nos diagramas e na wiki.
- **As regras do negócio ficam em `servicos.py`**, não na API nem nos ecrãs. A API só trata do HTTP.
- **Cada alteração de código traz testes.** Corre os testes do back-end e do front-end antes de abrir o pull request.
- **Não inventes requisitos.** Personas, cenários e user stories vêm das entrevistas no Character.ai e estão no Jira. Se faltar informação, pergunta à equipa.
- **Nunca ponhas palavras-passe, chaves de API nem o `.env`** no repositório.
- **Uma branch por cartão** (`feature/EDS-nn-nome`) e pull request revisto por outra pessoa. Ver [Git e pull requests](wiki/06-codigo/git.md).
- **Cada pessoa faz commit do seu trabalho com a sua conta.** Não se fazem commits em nome de outra pessoa.
- **Regista o uso de IA.** Se uma ferramenta de IA escreveu ou mudou alguma coisa, diz-se no pull request e acrescenta-se uma linha a `docs/registo-ia/registo_uso_ia.tex`.
- **Atualiza o [estado atual](wiki/currentstate.md)** quando acabares algo que mude o que lá está.

## Onde está cada coisa

| O quê | Onde |
|---|---|
| Índice da documentação | [wiki/README.md](wiki/README.md) |
| Arquitetura e decisões | [wiki/04-arquitetura/](wiki/04-arquitetura/arquitetura.md) |
| Diagramas UML | [wiki/05-modelacao/](wiki/05-modelacao/casos-de-uso.md) |
| Testes | [wiki/06-codigo/testes.md](wiki/06-codigo/testes.md) |
| Documentos entregues (PDF, LaTeX) | `docs/` |
