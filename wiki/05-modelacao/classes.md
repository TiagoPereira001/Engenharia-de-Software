# Diagrama de classes

[Índice](../README.md) · [← Casos de uso](casos-de-uso.md) · [Diagramas de sequência →](sequencia.md)

O FigJam não faz diagramas de classes, por isso este fica em Mermaid (o GitHub mostra-o como imagem). O modelo de dados com as tabelas está no [FigJam](https://www.figma.com/board/czxBO7U14mX4uEDGr29P41), diagrama 7.

Utilizador, Pedido, Categoria, Voto e MudancaEstado já existem no código (`backend/contas/models.py` e `backend/pedidos/models.py`). As outras são do desenho e entram nos próximos sprints.

```mermaid
classDiagram
    class Utilizador {
        username
        email
        papel
        gere_pedidos() bool
    }
    class Pedido {
        titulo
        descricao
        estado
        origem
        criado_em
    }
    class Categoria {
        nome
    }
    class Voto {
        criado_em
    }
    class MudancaEstado {
        de
        para
        motivo
        quando
    }
    class Comentario {
        texto
        criado_em
    }
    class UserStory {
        texto
    }
    class CriterioAceitacao {
        texto
    }
    class Equipa {
        nome
    }
    class Sprint {
        nome
        inicio
        fim
    }
    class Release {
        nome
        data
    }
    class Notificacao {
        texto
        lida
    }
    Utilizador "1" --> "*" Pedido : submete
    Categoria "1" --> "*" Pedido : classifica
    Pedido "1" *-- "*" Voto
    Utilizador "1" --> "*" Voto : dá
    Pedido "1" *-- "*" MudancaEstado : histórico
    Pedido "1" *-- "*" Comentario
    Pedido "1" --> "*" UserStory : gera
    UserStory "1" *-- "*" CriterioAceitacao
    Sprint "1" o-- "*" UserStory
    Release "1" o-- "*" Pedido
    Equipa "1" o-- "*" Utilizador
    Utilizador "1" --> "*" Notificacao : recebe
```

Regras que o diagrama não mostra mas o código garante:

- um voto por pessoa e por pedido (restrição na base de dados);
- as mudanças de estado seguem o [diagrama de estados](estados-e-atividades.md).

## Ver também

- [Diagramas de sequência](sequencia.md)
- [Estrutura do código](../06-codigo/estrutura.md)
