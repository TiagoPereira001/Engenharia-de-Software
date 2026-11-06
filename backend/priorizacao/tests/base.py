from contas.models import Papel, Utilizador
from pedidos import servicos as pedidos
from pedidos.models import Categoria, Estado


class Dados:
    """Utilizadores e pedidos que todos os testes da priorização usam."""

    def setUp(self):
        self.sofia = Utilizador.objects.create_user("sofia", password="x", papel=Papel.CLIENTE)
        self.marta = Utilizador.objects.create_user("marta", password="x", papel=Papel.PRODUCT_MANAGER)
        self.ricardo = Utilizador.objects.create_user("ricardo", password="x", papel=Papel.PRODUCT_OWNER)
        self.diogo = Utilizador.objects.create_user("diogo", password="x", papel=Papel.PROGRAMADOR)
        self.cat = Categoria.objects.create(nome="Relatórios")

    def pedido(self, titulo, estado=Estado.APROVADO):
        pedido = pedidos.criar_pedido(autor=self.sofia, titulo=titulo, descricao="x", categoria=self.cat)
        if estado in (Estado.EM_ANALISE, Estado.APROVADO):
            pedidos.mudar_estado(pedido=pedido, para=Estado.EM_ANALISE, autor=self.marta)
        if estado == Estado.APROVADO:
            pedidos.mudar_estado(pedido=pedido, para=Estado.APROVADO, autor=self.marta)
        return pedido
