# Estados e atividades

[Índice](../README.md) · [← Diagramas de sequência](sequencia.md) · [Como correr o projeto →](../06-codigo/como-correr.md)

Diagramas 5 e 6 no [FigJam](https://www.figma.com/board/czxBO7U14mX4uEDGr29P41).

## Estados de um pedido

Os estados são os da US-12 ([EDS-120](https://ubi-team-ebw5rr6y.atlassian.net/browse/EDS-120)). O código recusa as transições que não estão aqui (`TRANSICOES` em `backend/pedidos/servicos.py`).

```mermaid
stateDiagram-v2
    [*] --> Novo: cliente submete
    Novo --> EmAnalise: product manager abre
    EmAnalise --> Aprovado
    EmAnalise --> Rejeitado: com motivo
    Aprovado --> EmDesenvolvimento: entra num sprint
    EmDesenvolvimento --> EmRevisao: pull request aberto
    EmRevisao --> EmDesenvolvimento: pede alterações
    EmRevisao --> Concluido: aceite pelo PO
    Rejeitado --> [*]
    Concluido --> [*]
```

## Atividades: triagem de um pedido

```mermaid
flowchart TD
    chega["Chega um pedido"] --> veio{"Veio pelo sistema?"}
    veio -->|Não| regista["PM regista com a origem"] --> igual
    veio -->|Sim| igual{"Já existe igual?"}
    igual -->|Sim| junta["Junta e soma o voto"] --> avisa
    igual -->|Não| analisa["Em análise"] --> decide{"Faz sentido?"}
    decide -->|Não| rejeita["Rejeita com motivo"] --> avisa
    decide -->|Sim| aprova["Aprova e estima"] --> crit{"Tem critérios?"}
    crit -->|Não| historias["Gera e revê user stories"] --> crit
    crit -->|Sim| backlog["Entra no backlog"] --> avisa
    avisa["Cliente é notificado"]
```

## Ver também

- [Diagrama de classes](classes.md)
- [Registo de decisões](../04-arquitetura/decisoes.md)
