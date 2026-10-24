# Casos de uso

[Índice](../README.md) · [← Registo de decisões](../04-arquitetura/decisoes.md) · [Diagrama de classes →](classes.md)

Os ficheiros fonte de todos os diagramas estão em `docs/sprint-3/modelacao/` (Mermaid, um ficheiro por diagrama), para se poderem alterar e voltar a gerar.

Diagrama 2 no [FigJam](https://www.figma.com/board/czxBO7U14mX4uEDGr29P41). Aqui fica a mesma informação em texto.

```mermaid
flowchart LR
    cliente["Cliente"] --- uc2(["Submeter pedido"])
    cliente --- uc4(["Votar"])
    cliente --- uc6(["Acompanhar o estado"])
    uc2 -.->|include| uc3(["Ver pedidos parecidos"])
    pm["Product manager"] --- uc8(["Mudar o estado"])
    pm --- uc14(["Planear releases e roadmap"])
    po["Product Owner"] --- uc9(["Priorizar o backlog"])
    uc9 -.->|extend| uc10(["Pedir sugestão de prioridade"])
    uc10 --- ia["Serviço de IA"]
    po --- uc12(["Planear o sprint"])
    po --- uc13(["Gerar user stories"])
    prog["Programador"] --- uc15(["Ver rastreabilidade"])
    gp["Gestor de projeto"] --- uc16(["Ver dashboard e carga"])
```

| Ator | Casos de uso |
|---|---|
| Cliente | Registar-se e entrar, submeter pedido (inclui ver parecidos), votar, pesquisar, acompanhar o estado, comentar |
| Product manager | Mudar o estado de um pedido, pesquisar, planear releases e roadmap |
| Product Owner | Priorizar (estende: pedir sugestão à IA), estimar impacto e esforço, planear o sprint, gerar user stories |
| Programador | Comentar e mencionar, estimar esforço, ver rastreabilidade |
| Gestor de projeto | Ver dashboard e carga das equipas, acompanhar o roadmap |
| Serviço de IA (externo) | Sugerir prioridades, propor user stories |

## Ver também

- [Diagrama de classes](classes.md)
- [User stories](../01-produto/user-stories.md)
