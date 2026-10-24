"""Testes às regras dos pedidos, sem passar pela API."""

from django.db import IntegrityError, transaction
from django.test import TestCase

from contas.models import Papel, Utilizador
from pedidos import servicos
from pedidos.models import Categoria, Estado, MudancaEstado, Origem, Voto


class Base(TestCase):
    def setUp(self):
        self.sofia = Utilizador.objects.create_user("sofia", password="x", papel=Papel.CLIENTE)
        self.marta = Utilizador.objects.create_user("marta", password="x", papel=Papel.PRODUCT_MANAGER)
        self.cat = Categoria.objects.create(nome="Relatórios")

    def novo(self, titulo="Exportação de relatórios em PDF", descricao="Para mandar à direção."):
        return servicos.criar_pedido(autor=self.sofia, titulo=titulo, descricao=descricao, categoria=self.cat)


class CriarPedido(Base):
    def test_nasce_novo_e_fica_no_historico(self):
        pedido = self.novo()
        self.assertEqual(pedido.estado, Estado.NOVO)
        linha = MudancaEstado.objects.get(pedido=pedido)
        self.assertEqual((linha.de, linha.para, linha.autor), ("", Estado.NOVO, self.sofia))

    def test_cliente_nao_escolhe_a_origem(self):
        pedido = servicos.criar_pedido(
            autor=self.sofia, titulo="Ligação ao Slack", descricao="x", categoria=self.cat, origem=Origem.EMAIL
        )
        self.assertEqual(pedido.origem, Origem.SISTEMA)

    def test_product_manager_regista_a_origem(self):
        pedido = servicos.criar_pedido(
            autor=self.marta, titulo="Ligação ao Slack", descricao="x", categoria=self.cat, origem=Origem.REUNIAO
        )
        self.assertEqual(pedido.origem, Origem.REUNIAO)


class MudarEstado(Base):
    def test_segue_o_diagrama_de_estados(self):
        pedido = self.novo()
        for estado in [Estado.EM_ANALISE, Estado.APROVADO, Estado.EM_DESENVOLVIMENTO, Estado.EM_REVISAO, Estado.CONCLUIDO]:
            servicos.mudar_estado(pedido=pedido, para=estado, autor=self.marta)
        self.assertEqual(pedido.estado, Estado.CONCLUIDO)
        self.assertEqual(pedido.historico.count(), 6)

    def test_recusa_transicao_impossivel(self):
        pedido = self.novo()
        with self.assertRaises(servicos.RegraViolada):
            servicos.mudar_estado(pedido=pedido, para=Estado.CONCLUIDO, autor=self.marta)
        self.assertEqual(pedido.estado, Estado.NOVO)

    def test_rejeitar_exige_motivo(self):
        pedido = self.novo()
        servicos.mudar_estado(pedido=pedido, para=Estado.EM_ANALISE, autor=self.marta)
        with self.assertRaises(servicos.RegraViolada):
            servicos.mudar_estado(pedido=pedido, para=Estado.REJEITADO, autor=self.marta, motivo="  ")
        servicos.mudar_estado(pedido=pedido, para=Estado.REJEITADO, autor=self.marta, motivo="Fora do âmbito")
        self.assertEqual(pedido.historico.last().motivo, "Fora do âmbito")


class Votos(Base):
    def test_votar_outra_vez_retira_o_voto(self):
        pedido = self.novo()
        self.assertTrue(servicos.alternar_voto(pedido=pedido, utilizador=self.marta))
        self.assertFalse(servicos.alternar_voto(pedido=pedido, utilizador=self.marta))
        self.assertEqual(pedido.votos.count(), 0)

    def test_base_de_dados_nao_aceita_voto_repetido(self):
        pedido = self.novo()
        Voto.objects.create(pedido=pedido, utilizador=self.marta)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Voto.objects.create(pedido=pedido, utilizador=self.marta)


class Parecidos(Base):
    def test_encontra_com_palavras_parecidas(self):
        alvo = self.novo()
        self.novo(titulo="Ligação ao Slack", descricao="Avisos no chat")
        encontrados = servicos.procurar_parecidos("exportar relatório")
        self.assertEqual(encontrados[0], alvo)
        self.assertEqual(len(encontrados), 1)

    def test_texto_curto_nao_procura(self):
        self.novo()
        self.assertEqual(servicos.procurar_parecidos("pdf"), [])

    def test_ignora_rejeitados(self):
        pedido = self.novo()
        servicos.mudar_estado(pedido=pedido, para=Estado.EM_ANALISE, autor=self.marta)
        servicos.mudar_estado(pedido=pedido, para=Estado.REJEITADO, autor=self.marta, motivo="Repetido")
        self.assertEqual(servicos.procurar_parecidos("exportar relatório"), [])
