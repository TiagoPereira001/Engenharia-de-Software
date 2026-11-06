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
- **Decisão:** SQLite em desenvolvimento. PostgreSQL entra no Sprint 4.
- **Atualização (24/10/2026):** o Docker entrou já no Sprint 3, com SQLite num volume, para a aplicação arrancar com um só comando.
- **Atualização (24/10/2026):** o projeto passou a correr todo em Docker, com PostgreSQL num contentor próprio (`db`). Sem Docker continua a ser SQLite, para quem não quer instalar nada, e a CI também testa em SQLite.
- **Consequência:** o aviso de parecidos usa, por agora, palavras em comum. Com PostgreSQL já disponível, a semelhança por trigramas pode entrar no Sprint 4.

## D4. A IA fica atrás de um adaptador (23/10/2026)

- **Contexto:** o Ricardo só aceita a IA se o sistema funcionar sem ela.
- **Decisão:** um único módulo fala com o serviço de IA, com tempo limite. Se falhar, a priorização manual continua.
- **Estado:** desenhado (diagrama de sequência 3) e implementado no Sprint 4, em `backend/priorizacao/ia.py`.
- **Como ficou (Sprint 4):** o serviço de IA é o Claude, da Anthropic, chamado com saída estruturada (JSON com nível e razão de cada pedido) e um tempo limite de 20 segundos. Só é usado quando há uma chave em `ANTHROPIC_API_KEY`. Sem chave, ou se o Claude falhar, recusar ou devolver uma resposta que não bate certo, a sugestão é feita por uma regra local (valor por ponto de esforço, a partir dos votos e do impacto), e o ecrã diz que a sugestão não veio da IA. Os títulos e os números dos pedidos são enviados ao serviço; as descrições e os nomes das pessoas não.

## D5. Os estados de um pedido são os da US-12 (23/10/2026)

- Novo, Em análise, Aprovado, Rejeitado, Em desenvolvimento, Em revisão, Concluído.
- Os mesmos nomes no Jira, nos diagramas, no código (`pedidos/models.py`) e nos ecrãs. Ver [estados](../05-modelacao/estados-e-atividades.md).

## D6. Escalas de impacto e de esforço (Sprint 4)

- **Contexto:** a US-09 pede uma escala fixa e documentada. Nos mockups o esforço aparecia como S, M e L, mas a equipa estima em pontos no Jira.
- **Decisão:** impacto em três níveis (1 Baixo, 2 Médio, 3 Alto); esforço em pontos da sequência de Fibonacci (1, 2, 3, 5, 8, 13), a mesma escala do Jira. A relação impacto/esforço serve para ordenar.
- **Consequência:** a capacidade do sprint passa a ser em pontos, e o aviso de capacidade (US-06) soma os pontos dos pedidos já ordenados. Os mockups do ecrã 05 passam a mostrar pontos.

## Ver também

- [Arquitetura](arquitetura.md)
