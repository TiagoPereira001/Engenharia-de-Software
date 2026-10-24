"""O front-end chega à API através do proxy do Vite (localhost:5173).

O Django tem de aceitar os POST vindos dessa origem, e só dessa.
"""

from django.test import override_settings
from rest_framework.test import APIClient, APITestCase

from contas.models import Utilizador
from pedidos import servicos
from pedidos.models import Categoria


# Como no Docker: o pedido chega ao contentor "backend" vindo do front-end em localhost:5173.
@override_settings(ALLOWED_HOSTS=["localhost", "testserver", "backend"])
class OrigemDoFrontEnd(APITestCase):
    def setUp(self):
        self.sofia = Utilizador.objects.create_user("sofia", password="segredo-comprido")
        cat = Categoria.objects.create(nome="Relatórios")
        self.pedido = servicos.criar_pedido(autor=self.sofia, titulo="Exportar em PDF", descricao="x", categoria=cat)
        self.cliente = APIClient(enforce_csrf_checks=True)
        self.cliente.get("/api/contas/eu/")
        self.cliente.post("/api/contas/entrar/", {"username": "sofia", "password": "segredo-comprido"}, format="json")

    def votar_vindo_de(self, origem):
        token = self.cliente.cookies["csrftoken"].value
        return self.cliente.post(
            f"/api/pedidos/{self.pedido.id}/voto/", HTTP_X_CSRFTOKEN=token, HTTP_ORIGIN=origem, HTTP_HOST="backend:8000"
        )

    def test_aceita_o_front_end(self):
        self.assertEqual(self.votar_vindo_de("http://localhost:5173").status_code, 200)

    def test_recusa_outra_origem(self):
        self.assertEqual(self.votar_vindo_de("http://site-estranho.example").status_code, 403)
