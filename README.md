# Engenharia de Software

Trabalho de grupo da UBI, 2026/27. Docentes: Nuno Pombo e Carlos Cunha.

O dia a dia está no Jira. Aqui ficam o código e os documentos. Quem chega agora começa por esta página, depois abre o Jira.

- [Jira, projeto EDS](https://ubi-team-ebw5rr6y.atlassian.net/jira/software/projects/EDS/boards/3)
- [Confluence](https://ubi-team-ebw5rr6y.atlassian.net/wiki/spaces/EDS/overview)
- [Figma, wireframes](https://www.figma.com/design/VGH6pNIEVkvzY6QtVo8gcr)
- [FigJam, diagramas do Sprint 3](https://www.figma.com/board/czxBO7U14mX4uEDGr29P41)
- [Wiki do projeto](wiki/README.md) e [estado atual](wiki/currentstate.md)

## O que vamos construir

Um *Feature Request & Product Roadmap Management System*, o produto que o enunciado propõe: um sistema para gerir pedidos de funcionalidades e o roadmap de um produto. Dá para submeter pedidos, etiquetá-los, priorizar (à mão, por votos e com uma sugestão de IA), montar o backlog e o sprint, atribuir trabalho, ver o roadmap e as releases, gerar user stories a partir dos pedidos, comentar e ter dashboards (pedidos, lead time, cycle time, carga das equipas).

Há back-end e front-end. São precisas pelo menos 8 interfaces para além do login e do CRUD. A arquitetura tem de estar justificada, com wireframes e mockups. Os requisitos levantam-se com o Character.ai. Usamos pelo menos uma ferramenta de IA para programar, e esse uso fica no registo.

## Equipa

| Nome | Número |
|---|---|
| Felipe Fogaça | 53394 |
| João Vitor | 53396 |
| Marcus Fernandes | 52822 |
| Rui Machado | 53867 |
| Tiago Pereira | 55019 |

## Sprints

| Sprint | Datas | Product Owner | Scrum Master | O que se fez |
|---|---|---|---|---|
| 1 | 21 set a 14 out | Tiago Pereira | Rui Machado | Equipa, contrato, Jira, produto decidido, primeira proposta de personas, cenários e user stories |
| 2 | 12 a 23 out | Felipe Fogaça | João Vitor | Entrevistas às cinco personas no Character.ai, personas e user stories revistas, wireframes |
| 3 | 23 a 26 out | João Vitor | Marcus Fernandes | Requisitos não funcionais, arquitetura, modelação UML, wireframes corrigidos, mockups, base do código |
| 4 | por confirmar | Marcus Fernandes | Felipe Fogaça | Primeiro incremento a funcionar (pedidos, votos, aviso de pedidos parecidos) |
| 5 | por confirmar | Rui Machado | Tiago Pereira | Restantes interfaces, testes, deploy e entrega final |

Cada um é Product Owner uma vez e Scrum Master uma vez, nunca os dois no mesmo sprint. A apresentação oral é no fim de cada sprint. A do Sprint 1 e a do Sprint 2 fizeram-se juntas, porque é o mesmo produto.

## O que está neste repositório

| Pasta | O que é |
|---|---|
| `wiki/` | Documentação em Markdown, por ordem: produto, requisitos, protótipo, arquitetura, modelação, código e Scrum. Começa no [índice](wiki/README.md). |
| `backend/` | Servidor Django REST Framework (módulos `contas` e `pedidos`) e os seus testes. Ver [como correr](wiki/06-codigo/como-correr.md). |
| `frontend/` | Aplicação React com os 15 ecrãs dos wireframes, numa versão inicial sem cores, e os seus testes. |
| `.github/workflows/` | Integração contínua: corre os testes em cada pull request. |
| `AGENTS.md` | Regras para quem trabalha no repositório, pessoas ou ferramentas de IA. |
| `docs/contrato/` | Contrato de equipa. O texto certo é o `.tex`. O PDF é uma compilação antiga: ainda diz Filipe, Marcus Bernardo, Sprint 1 até 9 de outubro e a branch `dev`. Falta compilar o `.tex` no Overleaf. |
| `docs/sprint-1/` | Análise do produto. `produto_personas_cenarios.pdf` e `analise_produto.tex` são a versão de 17 de outubro: produto, papéis, sete áreas, personas, cenários e user stories. `analise_produto.pdf` é a primeira versão, de 28 de setembro, sobre uma aplicação da UBI que era o exercício do Lab03 e não o produto do enunciado; fica como histórico. |
| `docs/sprint-2/` | Guião das entrevistas no Character.ai (`entrevistas_character_ai.pdf`) e os primeiros rascunhos dos ecrãs (`wireframes_exemplos.pdf`). Os wireframes definitivos estão no Figma. |
| `docs/guia-jira/` | Guia para usar o nosso Jira, em LaTeX. |
| `docs/registo-ia/` | Onde registamos o uso de IA, em LaTeX. |
| `certificados-scrum/` | Print do Certiprof de cada um. |

Os documentos de 17 de outubro foram escritos antes das entrevistas. O que saiu delas (as cinco personas revistas, os cenários e as user stories corrigidas) está no Jira, nos epics Personas (EDS-150), Cenários (EDS-151) e User stories (EDS-152), com as capturas e o texto de cada conversa no cartão EDS-55.

Os documentos do Sprint 3 em LaTeX (requisitos não funcionais, arquitetura e modelação) vão para `docs/sprint-3/`. A versão de trabalho está na `wiki/`.

Os `.tex` compilam no Overleaf com pdfLaTeX. É preciso compilar duas vezes para os números de página ficarem certos.

## Como trabalhamos no Git

Há uma branch, a `main`. Cada tarefa sai numa branch à parte, com a chave do cartão, e volta por pull request. Outra pessoa da equipa revê antes de integrar.

```bash
git switch main
git pull
git switch -c feature/EDS-164-ambiente
```

A chave vai em maiúsculas na branch, no commit e no título do pull request. Passwords e chaves de API não entram no repositório.

## Avaliação

| Parte | Peso |
|---|---|
| C1, aplicação do Scrum | 15% |
| C2, participação e apresentações orais | 40% |
| C3, princípios de engenharia de software | 45% |
