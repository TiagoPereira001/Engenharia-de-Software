"""Cria utilizadores de teste e pedidos de exemplo para as demonstrações.

Só para desenvolvimento. A palavra-passe de cada utilizador de teste é o nome seguido de 123
(sofia / sofia123). Também cria o administrador admin / admin123 para entrar em /admin/.
"""

from django.core.management.base import BaseCommand

from contas.models import Papel, Utilizador
from pedidos import servicos
from pedidos.models import Categoria, Estado, Pedido

UTILIZADORES = [
    ("sofia", Papel.CLIENTE),
    ("marta", Papel.PRODUCT_MANAGER),
    ("ricardo", Papel.PRODUCT_OWNER),
    ("diogo", Papel.PROGRAMADOR),
    ("helena", Papel.GESTOR_PROJETO),
]

CATEGORIAS = ["Relatórios", "Integrações", "Usabilidade", "Desempenho", "Notificações"]

PEDIDOS = [
    ("Exportação de relatórios em PDF", "Queria exportar os relatórios mensais em PDF para mandar à direção.", "Relatórios"),
    ("Filtrar pedidos de reposição por data de validade", "Perco muito tempo a ver um por um. Um filtro por data de validade resolvia.", "Usabilidade"),
    ("Ligação ao Slack", "Receber no Slack os avisos quando um pedido muda de estado.", "Integrações"),
    ("Lista de pedidos mais rápida", "A lista demora a abrir quando há muitos pedidos.", "Desempenho"),
    ("Aviso por email quando o pedido é lido", "Quero saber quando alguém lê o meu pedido, sem ter de perguntar.", "Notificações"),
]


def palavra_passe_teste(nome):
    return f"{nome}123"


class Command(BaseCommand):
    help = "Cria utilizadores de teste e pedidos de exemplo (só para desenvolvimento)."

    def handle(self, *args, **options):
        pessoas = {}
        for nome, papel in UTILIZADORES:
            u, _ = Utilizador.objects.get_or_create(username=nome, defaults={"papel": papel})
            # Repõe sempre a palavra-passe, para quem já tinha a base de dados criada.
            u.set_password(palavra_passe_teste(nome))
            u.save()
            pessoas[nome] = u

        admin, _ = Utilizador.objects.get_or_create(
            username="admin", defaults={"papel": Papel.PRODUCT_MANAGER, "is_staff": True, "is_superuser": True}
        )
        admin.set_password(palavra_passe_teste("admin"))
        admin.save()

        cats = {nome: Categoria.objects.get_or_create(nome=nome)[0] for nome in CATEGORIAS}

        if Pedido.objects.exists():
            self.stdout.write("Já há pedidos; não criei mais.")
            return
        for titulo, descricao, cat in PEDIDOS:
            servicos.criar_pedido(autor=pessoas["sofia"], titulo=titulo, descricao=descricao, categoria=cats[cat])

        primeiro = Pedido.objects.get(titulo__startswith="Exportação")
        servicos.mudar_estado(pedido=primeiro, para=Estado.EM_ANALISE, autor=pessoas["marta"])
        for nome in ["marta", "diogo", "helena"]:
            servicos.alternar_voto(pedido=primeiro, utilizador=pessoas[nome])
        self.stdout.write(self.style.SUCCESS(f"Pronto. Utilizadores: {', '.join(pessoas)} e admin (palavra-passe: nome + 123)."))
