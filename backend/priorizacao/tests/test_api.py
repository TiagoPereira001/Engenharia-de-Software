"""Testes à API da priorização: o que o ecrã 05 chama."""

from rest_framework.test import APITestCase

from priorizacao import servicos

from .base import Dados


class ApiPriorizacao(Dados, APITestCase):
    def test_toda_a_equipa_ve_a_ordem(self):
        a = self.pedido("Exportar relatórios")
        resposta = self.client.get("/api/priorizacao/")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual([i["id"] for i in resposta.data["itens"]], [a.id])
        self.assertEqual(resposta.data["escala"]["esforco"], [1, 2, 3, 5, 8, 13])

    def test_product_owner_estima_e_ordena(self):
        a, b = self.pedido("Exportar relatórios"), self.pedido("Ligação ao Slack")
        self.client.force_authenticate(self.ricardo)
        estimativa = {"impacto": 3, "esforco": 5}
        resposta = self.client.patch(f"/api/priorizacao/{a.id}/estimativa/", estimativa, format="json")
        self.assertEqual(resposta.status_code, 200)
        ordem = {"ids": [b.id, a.id], "razao": "Pedido do cliente"}
        resposta = self.client.post("/api/priorizacao/ordem/", ordem, format="json")
        self.assertEqual([i["id"] for i in resposta.data["itens"]], [b.id, a.id])
        historico = self.client.get("/api/priorizacao/historico/").data
        self.assertEqual((historico[0]["autor"], historico[0]["razao"]), ("ricardo", "Pedido do cliente"))

    def test_esforco_fora_da_escala_da_erro(self):
        a = self.pedido("Exportar relatórios")
        self.client.force_authenticate(self.ricardo)
        resposta = self.client.patch(f"/api/priorizacao/{a.id}/estimativa/", {"esforco": 4}, format="json")
        self.assertEqual(resposta.status_code, 400)

    def test_cliente_nao_ordena(self):
        a = self.pedido("Exportar relatórios")
        self.client.force_authenticate(self.sofia)
        resposta = self.client.post("/api/priorizacao/ordem/", {"ids": [a.id]}, format="json")
        self.assertEqual(resposta.status_code, 403)

    def test_capacidade_vem_no_endereco(self):
        a = self.pedido("Exportar relatórios")
        servicos.estimar(pedido=a, autor=self.ricardo, esforco=13)
        servicos.ordenar(autor=self.ricardo, ids=[a.id])
        resposta = self.client.get("/api/priorizacao/", {"capacidade": 10})
        self.assertIn("13 pontos", resposta.data["aviso"])

    def test_sugestao_so_para_o_product_owner(self):
        self.pedido("Exportar relatórios")
        self.client.force_authenticate(self.marta)
        self.assertEqual(self.client.get("/api/priorizacao/sugestao/").status_code, 403)
        self.client.force_authenticate(self.ricardo)
        resposta = self.client.get("/api/priorizacao/sugestao/")
        self.assertEqual(resposta.data["fonte"], "regra local")
        self.assertEqual(resposta.data["sugestoes"][0]["titulo"], "Exportar relatórios")
        self.assertTrue(resposta.data["sugestoes"][0]["razao"])
