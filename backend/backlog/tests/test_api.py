"""Testes à API do backlog: o que os ecrãs 06 e 07 chamam."""

from rest_framework.test import APITestCase

from backlog import servicos

from .base import Dados


class ApiBacklog(Dados, APITestCase):
    def por(self, sprint_id, pedido_id):
        return self.client.post(f"/api/backlog/sprints/{sprint_id}/itens/", {"pedido": pedido_id}, format="json")

    def test_product_owner_acrescenta_ao_backlog(self):
        pedido = self.aprovado("Exportar relatórios")
        self.client.force_authenticate(self.ricardo)
        resposta = self.client.post("/api/backlog/", {"pedido": pedido.id}, format="json")
        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.data["itens"][0]["motivo"], "sem estimativa: não pode entrar")

    def test_criar_sprint_e_planear(self):
        item = self.no_backlog("Exportar relatórios", esforco=5)
        self.client.force_authenticate(self.ricardo)
        novo = {"nome": "Sprint 4", "objetivo": "Priorizar", "inicio": "2026-11-09", "fim": "2026-11-20"}
        novo["capacidade"] = 4
        sprint = self.client.post("/api/backlog/sprints/", novo, format="json").data
        resposta = self.por(sprint["id"], item.pedido_id)
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.data["pontos"], 5)
        self.assertIn("capacidade é 4", resposta.data["aviso"])
        resposta = self.client.delete(f"/api/backlog/sprints/{sprint['id']}/itens/{item.pedido_id}/")
        self.assertEqual(resposta.data["itens"], [])

    def test_sem_estimativa_da_erro_claro(self):
        item = self.no_backlog("Exportar relatórios")
        sprint = self.sprint()
        self.client.force_authenticate(self.ricardo)
        resposta = self.por(sprint.id, item.pedido_id)
        self.assertEqual(resposta.status_code, 400)
        self.assertIn("sem estimativa", resposta.data["erro"])

    def test_quadro_diz_o_que_cada_um_pode_fazer(self):
        sprint = self.sprint()
        item = self.no_backlog("Exportar relatórios", esforco=3)
        servicos.por_no_sprint(item=item, sprint=sprint, autor=self.ricardo)
        self.client.force_authenticate(self.diogo)
        quadro = self.client.get(f"/api/backlog/sprints/{sprint.id}/quadro/").data
        aprovado = quadro["colunas"][0]
        self.assertEqual(aprovado["nome"], "Aprovado")
        self.assertEqual(aprovado["itens"][0]["pode_mudar_para"], ["em_desenvolvimento"])

    def test_programador_nao_planeia(self):
        sprint = self.sprint()
        item = self.no_backlog("Exportar relatórios", esforco=3)
        self.client.force_authenticate(self.diogo)
        resposta = self.por(sprint.id, item.pedido_id)
        self.assertEqual(resposta.status_code, 403)

    def test_fechar_devolve_quantos_voltaram(self):
        sprint = self.sprint()
        item = self.no_backlog("Exportar relatórios", esforco=3)
        servicos.por_no_sprint(item=item, sprint=sprint, autor=self.ricardo)
        self.client.force_authenticate(self.ricardo)
        self.client.post(f"/api/backlog/sprints/{sprint.id}/comecar/")
        resposta = self.client.post(f"/api/backlog/sprints/{sprint.id}/fechar/")
        self.assertEqual(resposta.data["voltaram_ao_backlog"], 1)

    def test_equipas_e_atribuir(self):
        item = self.no_backlog("Exportar relatórios")
        self.assertEqual(self.client.get("/api/backlog/equipas/").data, [{"id": self.equipa.id, "nome": "Equipa A"}])
        self.client.force_authenticate(self.helena)
        dados = {"equipa": self.equipa.id}
        resposta = self.client.patch(f"/api/backlog/{item.pedido_id}/equipa/", dados, format="json")
        self.assertEqual(resposta.data["equipa"]["nome"], "Equipa A")
