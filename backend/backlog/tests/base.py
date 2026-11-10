from datetime import date

from backlog import servicos
from backlog.models import Equipa
from contas.models import Papel, Utilizador
from pedidos import servicos as pedidos
from pedidos.models import Categoria, Estado
from priorizacao import servicos as priorizacao


class Dados:
    """Utilizadores, uma equipa e pedidos aprovados para os testes do backlog."""

    def setUp(self):
        self.sofia = Utilizador.objects.create_user("sofia", password="x", papel=Papel.CLIENTE)
        self.marta = Utilizador.objects.create_user("marta", password="x", papel=Papel.PRODUCT_MANAGER)
        self.ricardo = Utilizador.objects.create_user("ricardo", password="x", papel=Papel.PRODUCT_OWNER)
        self.diogo = Utilizador.objects.create_user("diogo", password="x", papel=Papel.PROGRAMADOR)
        self.helena = Utilizador.objects.create_user("helena", password="x", papel=Papel.GESTOR_PROJETO)
        self.cat = Categoria.objects.create(nome="Relatórios")
        self.equipa = Equipa.objects.create(nome="Equipa A")

    def aprovado(self, titulo, esforco=None):
        pedido = pedidos.criar_pedido(autor=self.sofia, titulo=titulo, descricao="x", categoria=self.cat)
        pedidos.mudar_estado(pedido=pedido, para=Estado.EM_ANALISE, autor=self.marta)
        pedidos.mudar_estado(pedido=pedido, para=Estado.APROVADO, autor=self.marta)
        if esforco:
            priorizacao.estimar(pedido=pedido, autor=self.ricardo, esforco=esforco)
        return pedido

    def no_backlog(self, titulo, esforco=None):
        return servicos.acrescentar_ao_backlog(pedido=self.aprovado(titulo, esforco), autor=self.ricardo)

    def sprint(self, capacidade=10):
        return servicos.criar_sprint(
            autor=self.ricardo, nome="Sprint 4", objetivo="Priorizar e planear",
            inicio=date(2026, 11, 9), fim=date(2026, 11, 20), capacidade=capacidade,
        )
