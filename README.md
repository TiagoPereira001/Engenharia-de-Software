# Engenharia de Software

Trabalho de grupo da UBI, 2026/27. Docentes: Nuno Pombo e Carlos Cunha.

O dia a dia está no Jira. Aqui ficam o código e os documentos. Quem chega agora começa por esta página, depois abre o Jira.

- [Jira, projeto EDS](https://ubi-team-ebw5rr6y.atlassian.net/jira/software/projects/EDS/boards/3)
- [Confluence](https://ubi-team-ebw5rr6y.atlassian.net/wiki/spaces/EDS/overview)

## O que vamos construir

O enunciado pede um sistema para gerir pedidos de funcionalidades e o roadmap de um produto. Dá para submeter pedidos, etiquetá-los, priorizar (à mão, por votos e com uma sugestão de IA), montar o backlog e o sprint, atribuir trabalho, ver o roadmap e as releases, gerar user stories a partir dos pedidos, comentar e ter dashboards (pedidos, lead time, cycle time, carga das equipas).

Há back-end e front-end. São precisas pelo menos 8 interfaces para além do login e do CRUD. A arquitetura tem de estar justificada, com wireframes e mockups. Os requisitos levantam-se com o Character.ai. Usamos pelo menos uma ferramenta de IA para programar, e esse uso fica no registo.

No Sprint 1 a análise de produto (personas, cenários, user stories e prioridades) foi escrita sobre uma aplicação universitária da UBI: horários, notas, propinas, avisos, mapa. Está em `docs/sprint-1/`. O enunciado descreve o sistema de pedidos e roadmap. As duas coisas coexistem até o professor fechar o tema. A decisão fica no Jira.

## Equipa

| Nome | Número |
|---|---|
| Felipe Fogaça | 53394 |
| João Vitor | 53396 |
| Marcus Fernandes | 52822 |
| Rui Machado | 53867 |
| Tiago Pereira | 55019 |

## Sprints

O professor deu mais uma semana a cada sprint do que as datas do enunciado. O Sprint 1 acaba a 14 de outubro. Daí para a frente são as datas do contrato.

| Sprint | Datas | Product Owner | Scrum Master |
|---|---|---|---|
| 1 | 21 set a 14 out | Tiago Pereira | Rui Machado |
| 2 | 12 a 30 out | Felipe Fogaça | João Vitor |
| 3 | 2 a 20 nov | João Vitor | Marcus Fernandes |
| 4 | 23 nov a 11 dez | Marcus Fernandes | Felipe Fogaça |
| 5 | 14 dez a 15 jan | Rui Machado | Tiago Pereira |

Cada um é Product Owner uma vez e Scrum Master uma vez, nunca os dois no mesmo sprint. A apresentação oral é na última semana do sprint.

No Jira, o Sprint 2 começa a 12 de outubro, por isso ainda se cruza com o fim do Sprint 1.

No fecho do Sprint 1 faltam, no quadro, a daily (EDS-4), a review (EDS-6) e a retrospetiva (EDS-7).

## O que já está neste repositório

| Pasta | O que é |
|---|---|
| `docs/contrato/` | Contrato de equipa. O texto certo é o `.tex`. O PDF ainda é uma compilação antiga: diz Filipe, Marcus Bernardo, Sprint 1 até 9 de outubro e a branch `dev`. Isso já foi corrigido no `.tex`, falta compilar no Overleaf. |
| `docs/sprint-1/` | Análise do produto do Sprint 1, em PDF e em LaTeX (`analise_produto`). |
| `docs/guia-jira/` | Guia para usar o nosso Jira, em LaTeX. |
| `docs/registo-ia/` | Onde registamos o uso de IA, em LaTeX. |
| `certificados-scrum/` | Print do Certiprof de cada um. |

Ainda não há código da aplicação. Wireframes, arquitetura, desenho, modelação e mockups entram aqui quando existirem, e ficam ligados no epic Artifacts do Jira (EDS-26 a EDS-30).

Os `.tex` compilam no Overleaf com pdfLaTeX. É preciso compilar duas vezes para os números de página ficarem certos.

## Como trabalhamos no Git

Há uma branch, a `main`. Cada tarefa sai numa branch à parte, com a chave do cartão, e volta por pull request. Outra pessoa da equipa revê antes de integrar.

```bash
git switch main
git pull
git switch -c feature/EDS-13-personas
```

A chave vai em maiúsculas na branch, no commit e no título do pull request. Passwords e chaves de API não entram no repositório.

## Avaliação

| Parte | Peso |
|---|---|
| C1, aplicação do Scrum | 15% |
| C2, participação e apresentações orais | 40% |
| C3, princípios de engenharia de software | 45% |
