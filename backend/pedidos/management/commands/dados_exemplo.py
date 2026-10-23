"""Cria utilizadores de teste e pedidos de exemplo para as demonstrações.

Só para desenvolvimento. A palavra-passe de todos os utilizadores de teste é a de baixo.
"""

from django.core.management.base import BaseCommand

from contas.models import Papel, Utilizador
from pedidos import servicos
from pedidos.models import Categoria, Estado, Pedido

PALAVRA_PASSE_TESTE = "teste-es-2026"

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


class Command(BaseCommand):
    help = "Cria utilizadores de teste e pedidos de exemplo (só para desenvolvimento)."

    def handle(self, *args, **options):
        pessoas = {}
        for nome, papel in UTILIZADORES:
            u, criado = Utilizador.objects.get_or_create(username=nome, defaults={"papel": papel})
            if criado:
                u.set_password(PALAVRA_PASSE_TESTE)
                u.save()
            pessoas[nome] = u
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
        self.stdout.write(self.style.SUCCESS(f"Pronto. Utilizadores: {', '.join(pessoas)}."))
