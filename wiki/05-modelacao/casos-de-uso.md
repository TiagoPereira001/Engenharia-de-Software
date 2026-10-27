# Casos de uso

[Índice](../README.md) · [← Registo de decisões](../04-arquitetura/decisoes.md) · [Diagrama de classes →](classes.md)

Um diagrama por ator, a partir das [user stories](../01-produto/user-stories.md), dos [cenários](../01-produto/cenarios.md), dos [wireframes](../03-prototipo/wireframes.md) e da [arquitetura](../04-arquitetura/arquitetura.md). Cada caso diz de onde vem (US, cenário ou ecrã). Os mesmos diagramas estão no [FigJam](https://www.figma.com/board/czxBO7U14mX4uEDGr29P41) (diagramas 2a a 2e) e os ficheiros fonte em `docs/sprint-3/modelacao/02-casos-de-uso-*.mmd`.

## 2a. Sofia Ferreira, cliente

Ecrãs 01, 02, 03, 04 e 12. Submeter pedido inclui sempre ver os parecidos (US-05).

```mermaid
flowchart LR
    sofia["Sofia Ferreira<br/>Cliente"]
    subgraph sistema ["Feature Request e Product Roadmap Management System"]
        uc1(["Registar-se e entrar<br/>US-30 · ecrã 01"])
        uc2(["Pesquisar e filtrar pedidos<br/>US-04 · ecrã 02"])
        uc3(["Submeter pedido<br/>US-01 · C1 · ecrã 03"])
        uc4(["Ver pedidos parecidos<br/>US-05"])
        uc5(["Votar num pedido<br/>US-07 · ecrãs 03 e 04"])
        uc6(["Acompanhar o estado do pedido<br/>C1 · ecrã 04"])
        uc7(["Comentar<br/>US-21 · ecrã 04"])
        uc8(["Receber notificação quando o estado muda<br/>US-22 · ecrã 12"])
    end
    nota["Só se mostra o total de votos, nunca quem votou."]
    sofia --- uc1
    sofia --- uc2
    sofia --- uc3
    sofia --- uc5
    sofia --- uc6
    sofia --- uc7
    sofia --- uc8
    uc3 -.->|"«include»"| uc4
    uc5 -.- nota
```

## 2b. Marta Lopes, product manager

Ecrãs 02, 03, 04, 08, 09 e 14. As etiquetas da US-02 ainda não têm classe no modelo; as versões da US-03 também não.

```mermaid
flowchart LR
    marta["Marta Lopes<br/>Product manager"]
    subgraph sistema ["Feature Request e Product Roadmap Management System"]
        uc1(["Pesquisar e filtrar pedidos<br/>US-04 · ecrã 02"])
        uc2(["Registar pedido com a origem<br/>triagem · ecrã 03"])
        uc3(["Categorizar e etiquetar o pedido<br/>US-02"])
        uc4(["Editar o pedido<br/>US-03 · ecrã 04"])
        uc5(["Mudar o estado de um pedido<br/>diagrama de estados · ecrã 04"])
        uc6(["Ver o roadmap<br/>US-14 · ecrã 08"])
        uc7(["Planear a release<br/>US-15 · C3 · ecrã 09"])
        uc8(["Ver pedidos submetidos, aprovados e rejeitados<br/>US-25 · ecrã 14"])
        uc9(["Ver funcionalidades por release<br/>US-26 · ecrã 14"])
    end
    n1["Origem: Sistema, Email, Reunião ou Chat."]
    n2["Abre de Novo para Em análise. Para rejeitar, tem de dar o motivo."]
    n3["Avisa quando há uma dependência por agendar.<br/>Inclui os milestones (US-16)."]
    marta --- uc1
    marta --- uc2
    marta --- uc3
    marta --- uc4
    marta --- uc5
    marta --- uc6
    marta --- uc7
    marta --- uc8
    marta --- uc9
    uc2 -.- n1
    uc5 -.- n2
    uc7 -.- n3
```

## 2c. Ricardo Almeida, Product Owner

Ecrãs 05, 06, 07 e 10. O Serviço de IA é ator secundário e só aparece aqui. Pedir sugestão estende a priorização: sem ela, o Ricardo prioriza à mão.

```mermaid
flowchart LR
    ricardo["Ricardo Almeida<br/>Product Owner"]
    subgraph sistema ["Feature Request e Product Roadmap Management System"]
        uc1(["Priorizar o backlog<br/>US-06 · ecrã 05"])
        uc2(["Pedir sugestão de prioridade<br/>US-08 · ecrã 05"])
        uc3(["Estimar impacto e esforço<br/>US-09 · ecrã 05"])
        uc4(["Planear o sprint<br/>US-10 e US-11 · ecrãs 06 e 07"])
        uc5(["Gerar user stories<br/>US-18 · C4 · ecrã 10"])
        uc6(["Aceitar a conclusão<br/>diagrama de estados"])
    end
    ia["Serviço de IA<br/>(externo)"]
    n1["A sugestão traz sempre a razão. Se a IA falhar ou passar dos 10 s, fica a ordem manual (D4, C2)."]
    n2["Avisa quando passa a capacidade. Sem estimativa ou sem critérios, o item não entra (C2)."]
    n3["O PO edita e aceita. Com pouca informação saem menos histórias e o sistema diz o que falta (C4)."]
    n4["Em revisão para Concluído."]
    ricardo --- uc1
    ricardo --- uc3
    ricardo --- uc4
    ricardo --- uc5
    ricardo --- uc6
    uc2 -.->|"«extend»"| uc1
    uc2 --- ia
    uc5 --- ia
    uc2 -.- n1
    uc4 -.- n2
    uc5 -.- n3
    uc6 -.- n4
```

## 2d. Diogo Martins, programador

Ecrãs 04, 07 e 11. A US-09 é do Ricardo, mas o Diogo também estima esforço. A US-19 é da Helena, mas o Diogo também consulta a rastreabilidade quando liga o trabalho ao pedido (C5).

```mermaid
flowchart LR
    diogo["Diogo Martins<br/>Programador"]
    subgraph sistema ["Feature Request e Product Roadmap Management System"]
        uc1(["Ver o estado e o histórico<br/>US-12 · ecrã 04"])
        uc2(["Comentar e mencionar<br/>US-21 e US-23 · C5 · ecrã 04"])
        uc3(["Estimar esforço"])
        uc4(["Ver dependências<br/>US-17"])
        uc5(["Ligar o trabalho ao pedido<br/>C5"])
        uc6(["Ver rastreabilidade<br/>ecrã 11"])
    end
    n1["Sem o pull request ligado, o pedido não passa a Concluído (C5)."]
    diogo --- uc1
    diogo --- uc2
    diogo --- uc3
    diogo --- uc4
    diogo --- uc5
    diogo --- uc6
    uc5 -.- n1
```

## 2e. Helena Costa, gestora de projeto

Ecrãs 08, 11, 13, 14 e 15.

```mermaid
flowchart LR
    helena["Helena Costa<br/>Gestora de projeto"]
    subgraph sistema ["Feature Request e Product Roadmap Management System"]
        uc1(["Acompanhar o roadmap<br/>US-29 · C6 · ecrã 08"])
        uc2(["Ver lead time e cycle time<br/>US-27 · ecrã 14"])
        uc3(["Ver a carga das equipas por tipo de trabalho<br/>US-28 · ecrã 15"])
        uc4(["Atribuir a equipas<br/>US-13"])
        uc5(["Ver o espaço da equipa<br/>US-24 · ecrã 13"])
        uc6(["Ver rastreabilidade<br/>US-19 · ecrã 11"])
    end
    n1["Primeiro as releases em risco e as entregas contratuais."]
    n2["Mostra as tarefas paradas há mais de 3 dias. Com dados em falta, a métrica aparece como incompleta (C6)."]
    helena --- uc1
    helena --- uc2
    helena --- uc3
    helena --- uc4
    helena --- uc5
    helena --- uc6
    uc1 -.- n1
    uc2 -.- n2
```

## Quem faz o quê

| Ator | Casos de uso |
|---|---|
| Sofia, cliente | Registar-se e entrar, pesquisar e filtrar, submeter pedido (inclui ver parecidos), votar, acompanhar o estado, comentar, receber notificações |
| Marta, product manager | Pesquisar e filtrar, registar pedido com a origem, categorizar e etiquetar, editar, mudar o estado, ver o roadmap, planear a release, ver submetidos/aprovados/rejeitados, ver funcionalidades por release |
| Ricardo, Product Owner | Priorizar o backlog (estende: pedir sugestão à IA), estimar impacto e esforço, planear o sprint, gerar user stories, aceitar a conclusão |
| Diogo, programador | Ver o estado e o histórico, comentar e mencionar, estimar esforço, ver dependências, ligar o trabalho ao pedido, ver rastreabilidade |
| Helena, gestora de projeto | Acompanhar o roadmap, ver lead time e cycle time, ver a carga das equipas, atribuir a equipas, ver o espaço da equipa, ver rastreabilidade |
| Serviço de IA (externo) | Sugerir prioridades com a razão, propor user stories |

## Ver também

- [Diagrama de classes](classes.md)
- [User stories](../01-produto/user-stories.md)
