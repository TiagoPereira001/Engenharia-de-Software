"""Testes à API da colaboração: o que o detalhe do pedido e o ecrã 12 chamam."""

from rest_framework.test import APITestCase

from colaboracao import servicos
from pedidos import servicos as pedidos
from pedidos.models import Estado

from .base import Dados


class ApiColaboracao(Dados, APITestCase):
    def url(self):
        return f"/api/colaboracao/pedidos/{self.pedido.id}/comentarios/"

    def test_ler_a_conversa_sem_conta_mas_comentar_precisa_de_conta(self):
        servicos.comentar(pedido=self.pedido, autor=self.ricardo, texto="Que colunas precisas?")
        self.assertEqual(self.client.get(self.url()).data[0]["autor"], "ricardo")
        self.assertEqual(self.client.post(self.url(), {"texto": "Olá"}, format="json").status_code, 403)

    def test_comentar_editar_e_apagar(self):
        self.client.force_authenticate(self.ricardo)
        criado = self.client.post(self.url(), {"texto": "Que colunas?"}, format="json").data
        self.assertTrue(criado["meu"])
        editado = self.client.patch(f"/api/colaboracao/comentarios/{criado['id']}/", {"texto": "Que colunas precisas?"})
        self.assertIsNotNone(editado.data["editado_em"])
        self.client.force_authenticate(self.diogo)
        self.assertEqual(self.client.delete(f"/api/colaboracao/comentarios/{criado['id']}/").status_code, 403)

    def test_notificacoes_e_marcar_todas_como_lidas(self):
        pedidos.mudar_estado(pedido=self.pedido, para=Estado.EM_ANALISE, autor=self.marta)
        self.client.force_authenticate(self.sofia)
        resposta = self.client.get("/api/colaboracao/notificacoes/")
        self.assertEqual(resposta.data["por_ler"], 1)
        self.assertEqual(resposta.data["itens"][0]["pedido"], self.pedido.id)
        resposta = self.client.post("/api/colaboracao/notificacoes/lidas/", {}, format="json")
        self.assertEqual(resposta.data["por_ler"], 0)

    def test_preferencias(self):
        self.client.force_authenticate(self.sofia)
        self.assertEqual(self.client.get("/api/colaboracao/preferencias/").data["email"], False)
        novas = {"estados": True, "mencoes": True, "comentarios": False, "email": True}
        self.assertEqual(self.client.put("/api/colaboracao/preferencias/", novas, format="json").data, novas)

    def test_pessoas_para_as_mencoes(self):
        self.client.force_authenticate(self.diogo)
        self.assertEqual(self.client.get("/api/colaboracao/pessoas/").data, ["diogo", "marta", "ricardo", "sofia"])
