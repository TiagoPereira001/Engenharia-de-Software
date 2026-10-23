# Registo de decisões

[Índice](../README.md) · [← Arquitetura](arquitetura.md) · [Casos de uso →](../05-modelacao/casos-de-uso.md)

Cada decisão importante fica aqui, com o contexto e as alternativas. Uma decisão nova acrescenta-se no fim; uma que mude não se apaga, marca-se como substituída.

## D1. Monólito modular (23/10/2026)

- **Contexto:** cinco pessoas, sete áreas de produto, pouco tempo de código.
- **Decisão:** um servidor Django com um módulo por área e uma API REST.
- **Alternativas:** microserviços; páginas geradas no servidor. Ver [arquitetura](arquitetura.md).
- **Consequências:** um só deploy; as fronteiras entre módulos têm de ser respeitadas à mão (um módulo não mexe nas tabelas de outro).

## D2. Django + React (23/10/2026)

- **Contexto:** o enunciado recomenda Django, React ou Node.js.
- **Decisão:** Django REST Framework no servidor, React (Vite) no browser.
- **Porquê:** o Django já traz autenticação, permissões, painel de administração e migrações, e isso poupa tempo no que não conta para as oito interfaces. O React tem bibliotecas prontas para arrastar e para gráficos.

## D3. SQLite agora, PostgreSQL depois (23/10/2026)

- **Contexto:** o pedido do Tiago foi uma base "muito simples, só para começar".
- **Decisão:** SQLite em desenvolvimento. PostgreSQL e Docker entram no Sprint 4.
- **Consequência:** o aviso de parecidos usa, por agora, palavras em comum. Com PostgreSQL passa a semelhança por trigramas.

## D4. A IA fica atrás de um adaptador (23/10/2026)

- **Contexto:** o Ricardo só aceita a IA se o sistema funcionar sem ela.
- **Decisão:** um único módulo fala com o serviço de IA, com tempo limite. Se falhar, a priorização manual continua.
- **Estado:** desenhado (diagrama de sequência 4), por implementar no Sprint 4.

## D5. Os estados de um pedido são os da US-12 (23/10/2026)

- Novo, Em análise, Aprovado, Rejeitado, Em desenvolvimento, Em revisão, Concluído.
- Os mesmos nomes no Jira, nos diagramas, no código (`pedidos/models.py`) e nos ecrãs. Ver [estados](../05-modelacao/estados-e-atividades.md).

## Ver também

- [Arquitetura](arquitetura.md)
