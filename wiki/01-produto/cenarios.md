# Cenários

[Índice](../README.md) · [← Personas](personas.md) · [User stories →](user-stories.md)

Cada cenário conta uma situação real de uma persona e o que corre mal. O texto completo está no Jira, no epic [EDS-151](https://ubi-team-ebw5rr6y.atlassian.net/browse/EDS-151).

| Cenário | Persona | Resumo | Quando corre mal |
|---|---|---|---|
| C1 [EDS-143](https://ubi-team-ebw5rr6y.atlassian.net/browse/EDS-143) | Sofia | Escreve um pedido, vê que já existe um parecido e vota nele. No dia seguinte sabe que passou a Em análise. | Se ignorar o aviso, o duplicado pode ser junto ao original e os votos passam para lá. |
| C2 [EDS-144](https://ubi-team-ebw5rr6y.atlassian.net/browse/EDS-144) | Ricardo | Prioriza com impacto, esforço e a sugestão da IA com razões. O sistema avisa quando passa a capacidade. | Sem IA, prioriza à mão. Sem estimativa, o pedido não entra no sprint. |
| C3 [EDS-145](https://ubi-team-ebw5rr6y.atlassian.net/browse/EDS-145) | Marta | Monta a release 2.0 e o sistema avisa de uma dependência por agendar. | Dependências circulares são recusadas. |
| C4 [EDS-146](https://ubi-team-ebw5rr6y.atlassian.net/browse/EDS-146) | Ricardo | Gera user stories a partir de um pedido aprovado, edita e aceita. | Pedido com pouca informação gera menos histórias e diz o que falta. |
| C5 [EDS-147](https://ubi-team-ebw5rr6y.atlassian.net/browse/EDS-147) | Diogo | Trabalha numa funcionalidade, comenta, menciona e liga o pull request. | Não dá para concluir sem pull request ligado. |
| C6 [EDS-148](https://ubi-team-ebw5rr6y.atlassian.net/browse/EDS-148) | Helena | Abre o dashboard antes da reunião com a direção e vê a release em risco. | Com dados em falta, a métrica aparece como incompleta. |

O primeiro incremento do código segue o C1.

## Ver também

- [User stories](user-stories.md)
- [Diagramas de sequência](../05-modelacao/sequencia.md)
