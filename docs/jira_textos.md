# Textos para colar no Jira

Tudo o que está dentro das caixas de código é para copiar e colar tal como está. A ordem é esta: primeiro os três epics, depois os cartões de registo, depois os cartões de trabalho do Sprint 1 e por fim o sprint. Os passos para criar cada coisa estão no guia de Jira.

Onde houver `[...]` é para preencher com o que realmente aconteceu.

## 1. Epics

Cria os três com o botão **Create**, tipo **Epic**.

### Team Contract

Summary:

```
Team Contract
```

Description:

```
Contrato de equipa do projeto de Engenharia de Software 2026/27.

Aqui ficam sempre as versões em vigor do contrato e do registo de uso de IA (anexos neste cartão). Quando o contrato mudar, anexamos a nova versão e comentamos o que mudou e porquê.

O contrato define:
- como são as reuniões (planning, daily, refinement, review e retrospetiva) e como as registamos
- as responsabilidades da equipa e de cada elemento, com a rotação de Product Owner e Scrum Master
- como resolvemos conflitos e o que acontece a quem não cumpre
- outras regras: comunicação, prazos, Definição de Concluído, uso do GitHub e uso responsável de IA

Rotação de Product Owner (PO) e Scrum Master (SM):
- Sprint 1 (21/09 a 09/10): PO Tiago Pereira, SM Filipe Fogaça
- Sprint 2 (12/10 a 30/10): PO Filipe Fogaça, SM João Vitor
- Sprint 3 (02/11 a 20/11): PO João Vitor, SM Marcus Bernardo
- Sprint 4 (23/11 a 11/12): PO Marcus Bernardo, SM Rui Machado
- Sprint 5 (14/12 a 15/01): PO Rui Machado, SM Tiago Pereira

Anexos: contrato_equipa.pdf, registo_uso_ia.pdf
```

Depois de criares o epic, anexa os dois PDF.

### Artifacts

Summary:

```
Artifacts
```

Description:

```
Ligações para tudo o que a equipa produz fora do Jira. Para cada artefacto grande há um cartão filho com o link ou o ficheiro.

- Repositório GitHub: https://github.com/TiagoPereira001/Engenharia-de-Software
- Wireframes: [link, quando existirem]
- Mockups: [link, quando existirem]
- Diagramas de modelação: [link, quando existirem]
- Documentação de arquitetura e design: [link, quando existirem]
```

### Daily SCRUM

Summary:

```
Daily SCRUM
```

Description:

```
Evidências do Scrum, sprint a sprint. Cada sprint tem quatro cartões filhos:
- Daily: um comentário por pessoa e por dia útil (feito, a fazer, bloqueios)
- Planning: ata do planning
- Review: ata da review, com o que foi aceite
- Retrospetiva: o que correu bem, o que correu mal e as melhorias

Estes cartões são só registos e não entram no sprint.
```

## 2. Cartões de registo (filhos do epic Daily SCRUM)

Para o Sprint 1 cria estes quatro. Nos outros sprints repete, mudando o número. **Não os metas dentro do sprint.**

### Daily – Sprint 1

Description:

```
Registo das dailies do Sprint 1. Cada pessoa escreve um comentário por dia útil, neste formato:

Dia dd/mm - Nome
Feito: ...
A fazer: ...
Bloqueios: ... (ou nenhum)

Quem não puder estar na reunião escreve o seu comentário no mesmo dia. O Scrum Master confirma, até ao fim do dia, que está tudo escrito.
```

### Planning – Sprint 1

Description:

```
Data: [dd/mm/aaaa]
Presentes: [nomes]
PO: Tiago Pereira | SM: Filipe Fogaça

Objetivo do sprint:
[uma frase]

Cartões escolhidos:
- [chave e título]

Decisões:
- [o que ficou decidido]

Ações:
- [o quê] - [quem] - [até quando]
```

### Review – Sprint 1

Description:

```
Data: [dd/mm/aaaa]
Presentes: [nomes]
PO: Tiago Pereira | SM: Filipe Fogaça

O objetivo do sprint foi cumprido? [sim / parcialmente / não]

Cartões aceites pelo PO:
- [chave e título]

Cartões não aceites (voltam ao backlog):
- [chave e título] - [porquê]

Notas:
- [o que surgiu durante a review]
```

### Retrospetiva – Sprint 1

Description:

```
Data: [dd/mm/aaaa]
Presentes: [nomes]

O que correu bem:
- [..]

O que correu mal:
- [..]

Melhorias para o próximo sprint:
- [melhoria] - [responsável]
```

## 3. Cartões de trabalho do Sprint 1

Isto é uma sugestão a partir do que existe no repositório e nas notas do Lab03. Ajustem ao que a equipa realmente fez. As estimativas em story points fazem-nas em conjunto no planning (planning poker). O estado só passa a *Done* se o trabalho estiver mesmo feito e aceite.

| Summary | Tipo | Epic | Descrição | Estado sugerido |
|---|---|---|---|---|
| Montar o Jira | Task | | Criar o projeto Scrum, convidar equipa e docentes, criar os epics e os cartões de registo. | In Progress |
| Escrever o contrato de equipa | Task | Team Contract | Contrato com reuniões, responsabilidades, conflitos e outras regras. Falta o grupo ler e concordar. | In Progress |
| Registo de uso de IA | Task | Team Contract | Ficheiro onde dizemos onde e para quê usamos IA no projeto. | In Progress |
| Criar o repositório no GitHub | Task | Artifacts | Repositório com as branches main e dev. | Done |
| Escolher a ferramenta de IA para programar | Task | Team Contract | Decidir qual usamos e registá-la no Registo de Uso de IA. | To Do |
| Definir stakeholders, features e personas | Task | | Primeira versão do Lab03: stakeholders, lista de features com prioridade e quatro personas. | Done |
| Escrever cenários e user stories | Story | | Cenários e user stories a partir das personas e das features. | To Do |
| Decidir o produto do grupo | Task | | Fechar qual é o produto antes de escrever o backlog de produto. | To Do |
| Certificado Scrum Foundation Professional | Task | | Cada elemento obtém o certificado e entrega-o no repositório do grupo. | To Do |

## 4. Sprint 1

Quando fores iniciar o sprint (**Start sprint**), usa estes valores. Muda as datas, porque o Jira preenche com o momento em que clicas.

Nome:

```
Sprint 1
```

Datas: 21/09/2026 a 09/10/2026

Sprint goal:

```
Pôr a equipa a funcionar: Jira montado, contrato de equipa escrito e primeira versão de personas, cenários e user stories. PO: Tiago Pereira | SM: Filipe Fogaça
```

## 5. Objetivos dos sprints seguintes

Para colar quando for a altura. São uma proposta para o PO de cada sprint ajustar no planning.

Sprint 2 (12/10 a 30/10):

```
Fechar os requisitos e ter os primeiros wireframes, com uma ideia clara da arquitetura. PO: Filipe Fogaça | SM: João Vitor
```

Sprint 3 (02/11 a 20/11):

```
Ter a arquitetura e o design documentados e o primeiro incremento a funcionar, com back-end e front-end ligados. PO: João Vitor | SM: Marcus Bernardo
```

Sprint 4 (23/11 a 11/12):

```
Construir o grosso das funcionalidades e das interfaces, com testes automáticos e integração contínua a correr. PO: Marcus Bernardo | SM: Rui Machado
```

Sprint 5 (14/12 a 15/01):

```
Fechar o projeto: acabar o que falta, limpar o código, fazer o deploy e preparar a entrega final. PO: Rui Machado | SM: Tiago Pereira
```

## 6. Comentário de cada daily

Para copiar, uma vez por dia útil, no cartão "Daily – Sprint N":

```
Dia dd/mm - Nome
Feito:
A fazer:
Bloqueios:
```
