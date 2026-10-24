# Diagramas de sequência

[Índice](../README.md) · [← Diagrama de classes](classes.md) · [Estados e atividades →](estados-e-atividades.md)

Diagramas 3 e 4 no [FigJam](https://www.figma.com/board/czxBO7U14mX4uEDGr29P41).

## Submeter um pedido com aviso de parecidos (cenário C1)

É o que está implementado na base do código.

```mermaid
sequenceDiagram
    actor Cliente
    participant UI as Novo pedido (React)
    participant API as API de pedidos
    participant S as servicos.py
    participant BD as Base de dados
    Cliente->>UI: escreve o título
    UI->>UI: espera 300 ms sem teclas
    UI->>API: GET /api/pedidos/parecidos/?q=...
    API->>S: procurar_parecidos(texto)
    S->>BD: pedidos com as mesmas palavras
    API-->>UI: até 5 pedidos
    alt o pedido já existe
        Cliente->>UI: Votar
        UI->>API: POST /api/pedidos/id/voto/
        API->>S: alternar_voto()
        API-->>UI: total de votos
    else é um pedido novo
        Cliente->>UI: Submeter
        UI->>API: POST /api/pedidos/
        API->>S: criar_pedido()
        S->>BD: pedido no estado Novo + linha no histórico
        API-->>UI: 201 com o pedido
    end
```

## Sugestão de prioridade quando a IA falha (cenário C2)

Desenhado para o Sprint 4.

```mermaid
sequenceDiagram
    actor PO as Product Owner
    participant UI as Priorização
    participant API as API de priorização
    participant A as Adaptador de IA
    participant IA as Serviço de IA
    PO->>UI: Pedir sugestão
    UI->>API: POST /api/priorizacao/sugestao
    API->>A: sugerir(pedidos)
    A->>IA: pedido com tempo limite de 10 s
    alt responde a tempo
        IA-->>A: ordem e razão de cada pedido
        API-->>UI: sugestão com razões
        PO->>UI: Aceitar ou Manter a minha ordem
    else falha ou passa o tempo
        A-->>API: sem sugestão
        API-->>UI: aviso; a priorização manual continua
    end
```

## Ver também

- [Estados e atividades](estados-e-atividades.md)
- [Cenários](../01-produto/cenarios.md)
