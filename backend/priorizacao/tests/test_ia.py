"""Testes à sugestão de prioridade (US-08). O serviço de IA nunca é chamado a sério nos testes."""

from unittest import mock

from django.test import SimpleTestCase

from priorizacao import ia

ITENS = [
    {"id": 1, "titulo": "Exportar relatórios", "votos": 4, "impacto": 3, "esforco": 5},
    {"id": 2, "titulo": "Aviso por email", "votos": 5, "impacto": 3, "esforco": 2},
    {"id": 3, "titulo": "Ligação ao Slack", "votos": 1, "impacto": 2, "esforco": 13},
]

RESPOSTA_IA = [
    {"pedido_id": 2, "nivel": "alta", "razao": "Esforço baixo para o valor que traz."},
    {"pedido_id": 1, "nivel": "alta", "razao": "Impacto alto e muitos votos."},
    {"pedido_id": 3, "nivel": "baixa", "razao": "Esforço muito alto."},
]


class RegraLocal(SimpleTestCase):
    def test_cada_sugestao_diz_porque(self):
        sugestoes = ia.sugerir_local(ITENS)
        self.assertEqual([s.pedido_id for s in sugestoes], [2, 1, 3])
        self.assertEqual([s.nivel for s in sugestoes], ["alta", "média", "baixa"])
        self.assertIn("esforço baixo", sugestoes[0].razao)
        self.assertTrue(all(s.razao for s in sugestoes))

    def test_sem_estimativa_diz_isso(self):
        sugestoes = ia.sugerir_local([{"id": 9, "titulo": "x", "votos": 0, "impacto": None, "esforco": None}])
        self.assertIn("sem estimativa", sugestoes[0].razao)


@mock.patch.dict("os.environ", {"ANTHROPIC_API_KEY": "chave-de-teste"})
class ComIA(SimpleTestCase):
    def test_usa_a_resposta_da_ia(self):
        with mock.patch.object(ia, "_pedir_ao_claude", return_value=RESPOSTA_IA):
            sugestoes, fonte = ia.sugerir(ITENS)
        self.assertEqual(fonte, "ia")
        self.assertEqual([s.pedido_id for s in sugestoes], [2, 1, 3])

    def test_se_a_ia_falhar_usa_a_regra_local(self):
        with mock.patch.object(ia, "_pedir_ao_claude", side_effect=TimeoutError("sem resposta")):
            with self.assertLogs("priorizacao.ia", level="WARNING"):
                sugestoes, fonte = ia.sugerir(ITENS)
        self.assertEqual(fonte, "regra local")
        self.assertEqual(len(sugestoes), 3)

    def test_resposta_incompleta_da_ia_nao_e_aceite(self):
        with mock.patch.object(ia, "_pedir_ao_claude", return_value=RESPOSTA_IA[:2]):
            with self.assertLogs("priorizacao.ia", level="WARNING"):
                _, fonte = ia.sugerir(ITENS)
        self.assertEqual(fonte, "regra local")


class SemChave(SimpleTestCase):
    @mock.patch.dict("os.environ", {}, clear=True)
    def test_sem_chave_nem_tenta_a_ia(self):
        with mock.patch.object(ia, "_pedir_ao_claude") as pedir:
            _, fonte = ia.sugerir(ITENS)
        pedir.assert_not_called()
        self.assertEqual(fonte, "regra local")
