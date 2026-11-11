from contas.models import Papel, Utilizador
from pedidos import servicos as pedidos
from pedidos.models import Categoria


class Dados:
    def setUp(self):
        self.sofia = Utilizador.objects.create_user("sofia", password="x", papel=Papel.CLIENTE)
        self.sofia.email = "sofia@exemplo.pt"
        self.sofia.save()
        self.marta = Utilizador.objects.create_user("marta", password="x", papel=Papel.PRODUCT_MANAGER)
        self.ricardo = Utilizador.objects.create_user("ricardo", password="x", papel=Papel.PRODUCT_OWNER)
        self.diogo = Utilizador.objects.create_user("diogo", password="x", papel=Papel.PROGRAMADOR)
        self.cat = Categoria.objects.create(nome="Relatórios")
        self.pedido = pedidos.criar_pedido(
            autor=self.sofia, titulo="Exportar relatórios", descricao="x", categoria=self.cat
        )
