# Apresentação do Sprint 4

[Índice](../README.md) · [← Sprint 4](sprint-4.md)

Falam o Product Owner (Marcus) e o Scrum Master (Felipe). Os outros três estão presentes para responder sobre o módulo que fizeram. O cartão é o [EDS-183](https://ubi-team-ebw5rr6y.atlassian.net/browse/EDS-183).

Antes de começar: `docker compose down -v` e depois `docker compose up --build`, para os dados de exemplo virem limpos (três pedidos aprovados, um backlog e o Sprint 4 por começar).

| # | Parte | Quem | Tempo | O que mostrar |
|---|---|---|---|---|
| 1 | Objetivo do sprint e o que entregámos | PO | 1 min | O objetivo no Jira e os oito ecrãs ligados à API |
| 2 | Priorizar | PO | 2,5 min | Entrar como `ricardo`. Ecrã 05: impacto e esforço, mudar a ordem com a razão, o aviso de capacidade, "Pedir sugestão" e a razão de cada sugestão |
| 3 | Planear e acompanhar o sprint | PO | 2 min | Ecrã 06: o item sem estimativa não entra, a barra de capacidade, "Começar sprint". Ecrã 07: o quadro, a equipa de cada cartão |
| 4 | Colaborar | PO | 1,5 min | Entrar como `diogo`, comentar com @sofia. Entrar como `sofia`: a notificação e o número no menu |
| 5 | Como está feito | SM | 2 min | [Desenho de software](../04-arquitetura/desenho.md): três camadas, dependências num só sentido, o sinal das notificações, o adaptador da IA |
| 6 | Qualidade | SM | 1,5 min | GitHub Actions: ruff, cobertura e testes; o refactoring do sprint |
| 7 | Como trabalhámos e reflexão | SM | 1,5 min | Jira (pontos planeados e feitos), commits de cada um, registo de IA, retrospetiva |

Passagem do PO para o SM: "Isto foi o que o sistema já faz. O Felipe explica como está feito e como trabalhámos."

## Frases-chave

- **Marcus:** "A ordem é do Product Owner. A IA só sugere, diz sempre porquê, e se falhar a priorização continua."
- **Marcus:** "Só entra no sprint o que tem estimativa. Ao fechar o sprint, o que não acabou volta ao backlog."
- **Felipe:** "Cada módulo tem três camadas e as regras ficam nos serviços. Por isso testamos as regras sem passar pela API."
- **Felipe:** "O ecrã não repete as regras: o servidor diz que botões cada papel pode ver."

## Perguntas que podem fazer

- **Porque é que a IA não decide sozinha?** Decisão D4: é um adaptador com tempo limite e uma regra local de reserva; nada muda sem o Product Owner aceitar.
- **Que dados vão para o serviço de IA?** Só os títulos e os números (votos, impacto, esforço). Nem descrições nem nomes de pessoas.
- **Porque pontos e não S, M, L?** Decisão D6: é a mesma escala do Jira, e a capacidade do sprint soma-se em pontos.
- **Como é que o módulo Pedidos avisa as pessoas sem depender da colaboração?** Decisão D7: um sinal do Django (padrão observador).
- **O que é a cobertura de 90 %?** A parte do código que os testes percorrem. Abaixo disso, o GitHub Actions fica vermelho.
- **O que fizeram de refactoring?** Ver a tabela no [desenho de software](../04-arquitetura/desenho.md).

## Ver também

- [Sprint 4](sprint-4.md)
