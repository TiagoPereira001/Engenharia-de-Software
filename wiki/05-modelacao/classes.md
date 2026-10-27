# Diagrama de classes

[Índice](../README.md) · [← Casos de uso](casos-de-uso.md) · [Diagramas de sequência →](sequencia.md)

O FigJam não faz diagramas de classes, por isso este fica em Mermaid (o GitHub mostra-o como imagem). Bate com o modelo de dados do [FigJam](https://www.figma.com/board/czxBO7U14mX4uEDGr29P41), diagrama 7. Os ficheiros fonte estão em `docs/sprint-3/modelacao/08-classes*.mmd`.

«no código» quer dizer que a classe já existe (`backend/contas/models.py` e `backend/pedidos/models.py`). «desenho» quer dizer que entra nos próximos sprints. O autor do pedido e o autor da mudança de estado aparecem como ligações a Utilizador ("submete" e "faz").

## Modelo completo

```mermaid
classDiagram
    class Utilizador {
        <<no código>>
        username
        email
        papel
        gere_pedidos() bool
    }
    class Categoria {
        <<no código>>
        nome
    }
    class Pedido {
        <<no código>>
        titulo
        descricao
        estado
        origem
        criado_em
        atualizado_em
    }
    class Voto {
        <<no código>>
        criado_em
    }
    class MudancaEstado {
        <<no código>>
        de
        para
        motivo
        quando
    }
    class Comentario {
        <<desenho>>
        texto
        criado_em
    }
    class UserStory {
        <<desenho>>
        texto
    }
    class CriterioAceitacao {
        <<desenho>>
        texto
    }
    class Equipa {
        <<desenho>>
        nome
    }
    class Sprint {
        <<desenho>>
        nome
        inicio
        fim
    }
    class Release {
        <<desenho>>
        nome
        data
    }
    class Notificacao {
        <<desenho>>
        texto
        lida
    }
    Utilizador "1" --> "*" Pedido : submete (autor)
    Categoria "1" --> "*" Pedido : classifica
    Pedido "1" *-- "*" Voto : recebe
    Utilizador "1" --> "*" Voto : dá
    Pedido "1" *-- "*" MudancaEstado : histórico
    Utilizador "1" --> "*" MudancaEstado : faz (autor)
    Pedido "1" *-- "*" Comentario : tem
    Utilizador "1" --> "*" Comentario : escreve
    Pedido "1" --> "*" UserStory : gera
    UserStory "1" *-- "*" CriterioAceitacao : tem
    Sprint "1" o-- "*" UserStory : inclui
    Release "1" o-- "*" Pedido : entrega
    Equipa "1" o-- "*" Utilizador : tem
    Utilizador "1" --> "*" Notificacao : recebe
```

Regras que o diagrama não mostra mas o código garante:

- um voto por pessoa e por pedido (restrição na base de dados);
- as mudanças de estado seguem o [diagrama de estados](estados-e-atividades.md).

## Por persona

Cada vista só tem as classes que a persona usa nos seus [casos de uso](casos-de-uso.md). Os nomes e as ligações são os do modelo completo.

### Sofia

A Sofia usa pedido, categoria, votos, histórico de estados, comentários e notificações.

```mermaid
classDiagram
    class Utilizador {
        <<no código>>
        username
        email
        papel
        gere_pedidos() bool
    }
    class Pedido {
        <<no código>>
        titulo
        descricao
        estado
        origem
        criado_em
        atualizado_em
    }
    class Categoria {
        <<no código>>
        nome
    }
    class Voto {
        <<no código>>
        criado_em
    }
    class MudancaEstado {
        <<no código>>
        de
        para
        motivo
        quando
    }
    class Comentario {
        <<desenho>>
        texto
        criado_em
    }
    class Notificacao {
        <<desenho>>
        texto
        lida
    }
    Utilizador "1" --> "*" Pedido : submete (autor)
    Categoria "1" --> "*" Pedido : classifica
    Pedido "1" *-- "*" Voto : recebe
    Utilizador "1" --> "*" Voto : dá
    Pedido "1" *-- "*" MudancaEstado : histórico
    Utilizador "1" --> "*" MudancaEstado : faz (autor)
    Pedido "1" *-- "*" Comentario : tem
    Utilizador "1" --> "*" Comentario : escreve
    Utilizador "1" --> "*" Notificacao : recebe
```

### Marta

A Marta usa pedido, categoria, histórico de estados, comentários e releases.

```mermaid
classDiagram
    class Utilizador {
        <<no código>>
        username
        email
        papel
        gere_pedidos() bool
    }
    class Pedido {
        <<no código>>
        titulo
        descricao
        estado
        origem
        criado_em
        atualizado_em
    }
    class Categoria {
        <<no código>>
        nome
    }
    class MudancaEstado {
        <<no código>>
        de
        para
        motivo
        quando
    }
    class Comentario {
        <<desenho>>
        texto
        criado_em
    }
    class Release {
        <<desenho>>
        nome
        data
    }
    Utilizador "1" --> "*" Pedido : submete (autor)
    Categoria "1" --> "*" Pedido : classifica
    Pedido "1" *-- "*" MudancaEstado : histórico
    Utilizador "1" --> "*" MudancaEstado : faz (autor)
    Pedido "1" *-- "*" Comentario : tem
    Utilizador "1" --> "*" Comentario : escreve
    Release "1" o-- "*" Pedido : entrega
```

### Ricardo

O Ricardo usa pedido, votos, histórico de estados, user stories, critérios de aceitação e sprints.

```mermaid
classDiagram
    class Utilizador {
        <<no código>>
        username
        email
        papel
        gere_pedidos() bool
    }
    class Pedido {
        <<no código>>
        titulo
        descricao
        estado
        origem
        criado_em
        atualizado_em
    }
    class Voto {
        <<no código>>
        criado_em
    }
    class MudancaEstado {
        <<no código>>
        de
        para
        motivo
        quando
    }
    class UserStory {
        <<desenho>>
        texto
    }
    class CriterioAceitacao {
        <<desenho>>
        texto
    }
    class Sprint {
        <<desenho>>
        nome
        inicio
        fim
    }
    Utilizador "1" --> "*" Pedido : submete (autor)
    Pedido "1" *-- "*" Voto : recebe
    Utilizador "1" --> "*" Voto : dá
    Pedido "1" *-- "*" MudancaEstado : histórico
    Utilizador "1" --> "*" MudancaEstado : faz (autor)
    Pedido "1" --> "*" UserStory : gera
    UserStory "1" *-- "*" CriterioAceitacao : tem
    Sprint "1" o-- "*" UserStory : inclui
```

### Diogo

O Diogo usa pedido, histórico de estados, comentários, user stories e critérios de aceitação.

```mermaid
classDiagram
    class Utilizador {
        <<no código>>
        username
        email
        papel
        gere_pedidos() bool
    }
    class Pedido {
        <<no código>>
        titulo
        descricao
        estado
        origem
        criado_em
        atualizado_em
    }
    class MudancaEstado {
        <<no código>>
        de
        para
        motivo
        quando
    }
    class Comentario {
        <<desenho>>
        texto
        criado_em
    }
    class UserStory {
        <<desenho>>
        texto
    }
    class CriterioAceitacao {
        <<desenho>>
        texto
    }
    Utilizador "1" --> "*" Pedido : submete (autor)
    Pedido "1" *-- "*" MudancaEstado : histórico
    Utilizador "1" --> "*" MudancaEstado : faz (autor)
    Pedido "1" *-- "*" Comentario : tem
    Utilizador "1" --> "*" Comentario : escreve
    Pedido "1" --> "*" UserStory : gera
    UserStory "1" *-- "*" CriterioAceitacao : tem
```

### Helena

A Helena usa equipas, pedido, histórico de estados, user stories, sprints e releases.

```mermaid
classDiagram
    class Utilizador {
        <<no código>>
        username
        email
        papel
        gere_pedidos() bool
    }
    class Equipa {
        <<desenho>>
        nome
    }
    class Pedido {
        <<no código>>
        titulo
        descricao
        estado
        origem
        criado_em
        atualizado_em
    }
    class MudancaEstado {
        <<no código>>
        de
        para
        motivo
        quando
    }
    class UserStory {
        <<desenho>>
        texto
    }
    class Release {
        <<desenho>>
        nome
        data
    }
    class Sprint {
        <<desenho>>
        nome
        inicio
        fim
    }
    Utilizador "1" --> "*" Pedido : submete (autor)
    Pedido "1" *-- "*" MudancaEstado : histórico
    Utilizador "1" --> "*" MudancaEstado : faz (autor)
    Pedido "1" --> "*" UserStory : gera
    Sprint "1" o-- "*" UserStory : inclui
    Release "1" o-- "*" Pedido : entrega
    Equipa "1" o-- "*" Utilizador : tem
```

A Helena atribui trabalho a equipas (US-13), mas o modelo ainda não diz o que fica ligado à equipa. Fica por decidir.

## Ver também

- [Diagramas de sequência](sequencia.md)
- [Estrutura do código](../06-codigo/estrutura.md)
