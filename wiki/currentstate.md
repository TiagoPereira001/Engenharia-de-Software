# Estado atual

[Índice](README.md) · [Visão do produto →](01-produto/visao.md)

Última atualização: 24 de outubro de 2026, Sprint 3.

Esta página diz onde o projeto está. Quem mexe no projeto (pessoa ou agente de IA) atualiza-a quando alguma coisa muda.

## Sprint em curso

**Sprint 3**, de 23 a 26 de outubro. Product Owner: João Vitor. Scrum Master: Marcus Fernandes.

Objetivo: requisitos não funcionais refeitos, arquitetura justificada, modelação UML, wireframes corrigidos e mockups, e a base do código a correr. As funcionalidades do primeiro incremento passam para o Sprint 4.

## Feito

- Personas, cenários e 29 user stories no Jira, revistos com as entrevistas no Character.ai. Ver [personas](01-produto/personas.md).
- Wireframes de baixa fidelidade dos 15 ecrãs no Figma, corrigidos a 23/10 com o que faltava das personas. Ver [wireframes](03-prototipo/wireframes.md).
- Diagramas para o Sprint 3 no FigJam: arquitetura, casos de uso, duas sequências, estados, atividades e modelo de dados. Fontes em `docs/sprint-3/modelacao/`. Ver [modelação](05-modelacao/casos-de-uso.md).
- Wireframes exportados em imagem para `docs/sprint-3/wireframes/`.
- Documento de requisitos não funcionais em LaTeX: `docs/sprint-3/requisitos_nao_funcionais.tex`.
- Base do código: back-end Django com contas e pedidos, front-end React com os 15 ecrãs e um estilo simples.
- Docker: `docker compose up --build` levanta o projeto inteiro (PostgreSQL, back-end e front-end) na mesma rede, com o código a recarregar sozinho. Ver [como correr](06-codigo/como-correr.md).
- Testes automáticos: 31 no back-end e 23 no front-end, todos a passar (também no PostgreSQL, dentro do Docker). Ver [testes](06-codigo/testes.md).
- Integração contínua (`.github/workflows/ci.yml`) a correr no GitHub em cada push e pull request.

## Por fazer neste sprint

- Rever, compilar no Overleaf e aceitar o documento de requisitos não funcionais ([EDS-159](https://ubi-team-ebw5rr6y.atlassian.net/browse/EDS-159)).
- Mockups dos ecrãs 01 a 04 ([EDS-163](https://ubi-team-ebw5rr6y.atlassian.net/browse/EDS-163)).
- Escrever o documento de arquitetura em LaTeX para `docs/sprint-3/` ([EDS-153](https://ubi-team-ebw5rr6y.atlassian.net/browse/EDS-153)), a partir de [arquitetura](04-arquitetura/arquitetura.md).
- Proteger a `main` no GitHub (só o Tiago tem permissões).
- Review, retrospetiva e apresentação ([EDS-173](https://ubi-team-ebw5rr6y.atlassian.net/browse/EDS-173)).

## Decisões em aberto

- Datas dos Sprints 4 e 5.
- Que serviço de IA usar na priorização (Sprint 4).

## Onde está cada coisa

| O quê | Onde |
|---|---|
| Trabalho do dia a dia | [Jira, projeto EDS](https://ubi-team-ebw5rr6y.atlassian.net/jira/software/projects/EDS/boards/3) |
| Wireframes | [Figma](https://www.figma.com/design/VGH6pNIEVkvzY6QtVo8gcr), página Baixa Fidelidade |
| Diagramas | [FigJam](https://www.figma.com/board/czxBO7U14mX4uEDGr29P41) |
| Documentos entregues (PDF, LaTeX) | `docs/` |
| Código | `backend/` e `frontend/` |
| Esta documentação | `wiki/` |

## Ver também

- [Índice da wiki](README.md)
- [Sprint 3](07-scrum/sprint-3.md)
- [AGENTS.md](../AGENTS.md)
