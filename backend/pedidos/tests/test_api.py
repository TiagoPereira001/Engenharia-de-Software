"""Testes à API dos pedidos: o que o front-end chama."""

from rest_framework.test import APITestCase

from contas.models import Papel, Utilizador
from pedidos import servicos
from pedidos.models import Categoria


class ApiPedidos(APITestCase):
    def setUp(self):
        self.sofia = Utilizador.objects.create_user("sofia", password="x", papel=Papel.CLIENTE)
        self.ricardo = Utilizador.objects.create_user("ricardo", password="x", papel=Papel.PRODUCT_OWNER)
        self.cat = Categoria.objects.create(nome="Relatórios")
        self.outra = Categoria.objects.create(nome="Integrações")

    def criar(self, titulo, categoria=None):
        return servicos.criar_pedido(autor=self.sofia, titulo=titulo, descricao="x", categoria=categoria or self.cat)

    def test_criar_pedido_precisa_de_login(self):
        resposta = self.client.post("/api/pedidos/", {"titulo": "Exportar em PDF", "descricao": "x", "categoria": self.cat.id})
        self.assertEqual(resposta.status_code, 403)

    def test_cliente_cria_pedido(self):
        self.client.force_authenticate(self.sofia)
        resposta = self.client.post("/api/pedidos/", {"titulo": "Exportar em PDF", "descricao": "x", "categoria": self.cat.id})
        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.data["estado"], "novo")
        self.assertEqual(resposta.data["autor"], "sofia")

    def test_titulo_curto_e_recusado(self):
        self.client.force_authenticate(self.sofia)
        resposta = self.client.post("/api/pedidos/", {"titulo": "PDF", "descricao": "x", "categoria": self.cat.id})
        self.assertEqual(resposta.status_code, 400)
        self.assertIn("titulo", resposta.data)

    def test_pesquisa_e_filtros_juntam_se(self):
        self.criar("Exportar relatórios")
        self.criar("Exportar contactos", self.outra)
        self.criar("Ligação ao Slack", self.outra)
        resposta = self.client.get("/api/pedidos/", {"q": "exportar", "categoria": self.outra.id})
        titulos = [p["titulo"] for p in resposta.data["results"]]
        self.assertEqual(titulos, ["Exportar contactos"])

    def test_votos_mostram_so_o_total(self):
        pedido = self.criar("Exportar relatórios")
        self.client.force_authenticate(self.sofia)
        resposta = self.client.post(f"/api/pedidos/{pedido.id}/voto/")
        self.assertEqual(resposta.data, {"votei": True, "total_votos": 1})
        detalhe = self.client.get(f"/api/pedidos/{pedido.id}/").data
        self.assertEqual(detalhe["total_votos"], 1)
        self.assertNotIn("votos", detalhe)

    def test_filtra_por_etiqueta(self):
        com = self.criar("Exportar relatórios")
        self.criar("Ligação ao Slack")
        servicos.classificar(pedido=com, autor=self.ricardo, etiquetas=["Excel"])
        resposta = self.client.get("/api/pedidos/", {"etiqueta": "excel"})
        self.assertEqual([p["titulo"] for p in resposta.data["results"]], ["Exportar relatórios"])
        self.assertEqual(resposta.data["results"][0]["etiquetas"], ["excel"])
        self.assertEqual(self.client.get("/api/etiquetas/").data, ["excel"])

    def test_os_meus_pedidos(self):
        self.criar("Exportar relatórios")
        servicos.criar_pedido(autor=self.ricardo, titulo="Pedido do Ricardo", descricao="x", categoria=self.cat)
        self.client.force_authenticate(self.sofia)
        resposta = self.client.get("/api/pedidos/", {"meus": "1"})
        self.assertEqual([p["titulo"] for p in resposta.data["results"]], ["Exportar relatórios"])

    def test_product_manager_classifica(self):
        pedido = self.criar("Exportar relatórios")
        self.client.force_authenticate(self.ricardo)
        resposta = self.client.patch(
            f"/api/pedidos/{pedido.id}/classificar/", {"categoria": self.outra.id, "etiquetas": ["Excel"]}, format="json"
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual((resposta.data["categoria"], resposta.data["etiquetas"]), (self.outra.id, ["excel"]))

    def test_cliente_nao_classifica(self):
        pedido = self.criar("Exportar relatórios")
        self.client.force_authenticate(self.sofia)
        resposta = self.client.patch(f"/api/pedidos/{pedido.id}/classificar/", {"etiquetas": ["x"]}, format="json")
        self.assertEqual(resposta.status_code, 403)

    def test_detalhe_diz_para_onde_se_pode_mudar(self):
        pedido = self.criar("Exportar relatórios")
        self.assertEqual(self.client.get(f"/api/pedidos/{pedido.id}/").data["pode_mudar_para"], [])
        self.client.force_authenticate(self.ricardo)
        self.assertEqual(self.client.get(f"/api/pedidos/{pedido.id}/").data["pode_mudar_para"], ["em_analise"])

    def test_cliente_nao_muda_o_estado(self):
        pedido = self.criar("Exportar relatórios")
        self.client.force_authenticate(self.sofia)
        resposta = self.client.post(f"/api/pedidos/{pedido.id}/estado/", {"para": "em_analise"})
        self.assertEqual(resposta.status_code, 403)

    def test_product_owner_muda_o_estado_e_fica_no_historico(self):
        pedido = self.criar("Exportar relatórios")
        self.client.force_authenticate(self.ricardo)
        resposta = self.client.post(f"/api/pedidos/{pedido.id}/estado/", {"para": "em_analise"})
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual([h["para"] for h in resposta.data["historico"]], ["novo", "em_analise"])

    def test_transicao_impossivel_da_erro_claro(self):
        pedido = self.criar("Exportar relatórios")
        self.client.force_authenticate(self.ricardo)
        resposta = self.client.post(f"/api/pedidos/{pedido.id}/estado/", {"para": "concluido"})
        self.assertEqual(resposta.status_code, 400)
        self.assertIn("erro", resposta.data)

    def test_parecidos_sem_login(self):
        self.criar("Exportação de relatórios em PDF")
        resposta = self.client.get("/api/pedidos/parecidos/", {"q": "exportar relatório"})
        self.assertEqual(len(resposta.data), 1)
