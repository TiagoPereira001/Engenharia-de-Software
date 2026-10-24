# Requisitos não funcionais

[Índice](../README.md) · [← Entrevistas no Character.ai](entrevistas.md) · [Wireframes →](../03-prototipo/wireframes.md)

Proposta para o Sprint 3 ([EDS-159](https://ubi-team-ebw5rr6y.atlassian.net/browse/EDS-159)). Cada requisito diz de onde vem e como se verifica. Os números ainda podem mudar na planning.

| Característica (ISO/IEC 25010) | Requisito | Vem de | Como se verifica |
|---|---|---|---|
| Usabilidade | Um cliente submete um pedido em 3 minutos ou menos | Sofia | Teste cronometrado com alguém de fora da equipa |
| Usabilidade | O formulário do cliente só pede título, descrição e uma categoria | Sofia | Teste automático do ecrã Novo pedido |
| Fiabilidade | Se a IA falhar ou demorar mais de 10 s, a priorização continua sem sugestão | Ricardo | Teste automático com o serviço desligado (Sprint 4) |
| Transparência | Cada sugestão da IA mostra a razão | Ricardo | Revisão do ecrã Priorização |
| Desempenho | Lista e pesquisa respondem em menos de 1 s com 1000 pedidos | Marta, Helena | Teste com dados gerados |
| Rastreabilidade | Todas as mudanças de estado ficam guardadas com data e autor | Ricardo, Helena | Testes automáticos ao histórico (já existem) |
| Segurança | Palavra-passe com hash; cada papel só faz o que lhe cabe | Enunciado | Testes de permissões (já existem) |
| Privacidade | Os votos mostram o total, nunca quem votou | Sofia | Teste automático à API (já existe) |
| Manutenibilidade | Testes automáticos em cada pull request; pelo menos 60% de cobertura no back-end | Equipa | GitHub Actions |
| Portabilidade | Arranca em qualquer máquina da equipa seguindo o README | Equipa | Um colega que não montou o ambiente experimenta |

A versão para entregar, com a especificação das user stories do primeiro incremento (entradas, regras e erros), está em LaTeX: `docs/sprint-3/requisitos_nao_funcionais.tex`.

Estes requisitos justificam as decisões da [arquitetura](../04-arquitetura/arquitetura.md).

## Ver também

- [Registo de decisões](../04-arquitetura/decisoes.md)
- [Testes](../06-codigo/testes.md)
