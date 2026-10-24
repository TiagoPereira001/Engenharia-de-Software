# Apresentação do Sprint 3

[Índice](../README.md) · [← Sprint 3](sprint-3.md)

Segunda-feira, 26 de outubro. Falam o Product Owner (João) e o Scrum Master (Marcus). Os outros três estão presentes para responder sobre a parte que fizeram. O cartão é o [EDS-173](https://ubi-team-ebw5rr6y.atlassian.net/browse/EDS-173).

| # | Parte | Quem | Tempo | O que mostrar |
|---|---|---|---|---|
| 1 | Objetivo e de onde partimos | PO | 1 min | [Personas](../01-produto/personas.md), [user stories](../01-produto/user-stories.md), wireframes |
| 2 | O que corrigimos do Sprint 2 | PO | 2 min | [Requisitos não funcionais](../02-requisitos/requisitos-nao-funcionais.md) |
| 3 | Wireframes corrigidos e mockups | PO | 2 min | Post-its "Sprint 3" no [Figma](https://www.figma.com/design/VGH6pNIEVkvzY6QtVo8gcr) |
| 4 | Arquitetura | SM | 2,5 min | Diagrama 1 no [FigJam](https://www.figma.com/board/czxBO7U14mX4uEDGr29P41) e a tabela das alternativas |
| 5 | Modelação UML | SM | 2 min | Diagramas 2 a 7 no FigJam e o [diagrama de classes](../05-modelacao/classes.md) |
| 6 | A base do código | SM | 1 min | Os 15 ecrãs sem cores, o aviso de parecidos a funcionar, os testes a passar (30 + 23) |
| 7 | Como trabalhámos e reflexão | SM | 1,5 min | Jira, burndown, registo de IA, retrospetiva |

Passagem do PO para o SM: "Isto foi o que mudámos no produto. O Marcus explica agora como o vamos construir e como trabalhámos."

## Regras

- Só se mostra o que está feito. O que faltar diz-se na reflexão, com o motivo.
- Os números (pontos planeados e feitos) são os reais do fim do sprint.
- Usar os mesmos nomes nos slides, nos diagramas, nos ecrãs e no código (por exemplo os estados da US-12).

## Perguntas que podem fazer

- **Porque não microserviços?** Ver [decisões](../04-arquitetura/decisoes.md), D1.
- **Isto escala?** O servidor não guarda estado entre pedidos, por isso pode ter várias cópias. O que é pesado (IA, emails) vai para tarefas em segundo plano.
- **Como garantem que a IA não decide sozinha?** Ver D4 e o diagrama de sequência 4.
- **Como evitam duplicados?** O aviso de parecidos enquanto se escreve, com voto em cada um.
- **Wireframe ou mockup?** Wireframe é estrutura; mockup é o aspeto final.

## Ver também

- [Sprint 3](sprint-3.md)
