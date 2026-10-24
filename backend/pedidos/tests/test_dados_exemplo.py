"""O comando dados_exemplo prepara as demonstrações; tem de funcionar sempre igual."""

from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from contas.models import Papel, Utilizador
from pedidos.models import Categoria, Estado, Pedido


class DadosExemplo(TestCase):
    def correr(self):
        call_command("dados_exemplo", stdout=StringIO())

    def test_cria_um_utilizador_por_papel(self):
        self.correr()
        papeis = set(Utilizador.objects.values_list("papel", flat=True))
        self.assertEqual(papeis, set(Papel.values))

    def test_cria_pedidos_com_historico_e_votos(self):
        self.correr()
        self.assertEqual(Pedido.objects.count(), 5)
        self.assertEqual(Categoria.objects.count(), 5)
        exportacao = Pedido.objects.get(titulo__startswith="Exportação")
        self.assertEqual(exportacao.estado, Estado.EM_ANALISE)
        self.assertEqual(exportacao.votos.count(), 3)
        self.assertEqual(exportacao.historico.count(), 2)

    def test_correr_duas_vezes_nao_duplica(self):
        self.correr()
        self.correr()
        self.assertEqual(Pedido.objects.count(), 5)
        self.assertEqual(Utilizador.objects.count(), 5)
