from rest_framework.test import APITestCase

from contas.models import Papel, Utilizador


class Contas(APITestCase):
    def test_quem_se_regista_fica_cliente(self):
        resposta = self.client.post(
            "/api/contas/registar/", {"username": "sofia", "email": "s@exemplo.pt", "password": "uma-frase-comprida"}
        )
        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.data["papel"], Papel.CLIENTE)

    def test_nao_da_para_escolher_o_papel_no_registo(self):
        self.client.post(
            "/api/contas/registar/",
            {"username": "x", "email": "x@exemplo.pt", "password": "uma-frase-comprida", "papel": "product_owner"},
        )
        self.assertEqual(Utilizador.objects.get(username="x").papel, Papel.CLIENTE)

    def test_palavra_passe_guardada_com_hash(self):
        Utilizador.objects.create_user("sofia", password="segredo-comprido")
        guardada = Utilizador.objects.get(username="sofia").password
        self.assertNotIn("segredo-comprido", guardada)

    def test_entrar_com_dados_errados_nao_diz_o_que_falhou(self):
        Utilizador.objects.create_user("sofia", password="segredo-comprido")
        errada = self.client.post("/api/contas/entrar/", {"username": "sofia", "password": "nao"})
        inexistente = self.client.post("/api/contas/entrar/", {"username": "ninguem", "password": "nao"})
        self.assertEqual(errada.status_code, 400)
        self.assertEqual(errada.data, inexistente.data)

    def test_eu_diz_quem_esta_autenticado(self):
        self.assertEqual(self.client.get("/api/contas/eu/").data, {"autenticado": False})
        Utilizador.objects.create_user("sofia", password="segredo-comprido")
        self.client.post("/api/contas/entrar/", {"username": "sofia", "password": "segredo-comprido"})
        self.assertEqual(self.client.get("/api/contas/eu/").data["utilizador"]["username"], "sofia")
