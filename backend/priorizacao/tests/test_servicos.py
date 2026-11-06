"""Testes às regras da priorização (US-06 e US-09)."""

from django.test import TestCase

from pedidos.models import Estado
from pedidos.servicos import SemPermissao, alternar_voto
from priorizacao import servicos
from priorizacao.models import AlteracaoOrdem

from .base import Dados


class Estimar(Dados, TestCase):
    def test_product_owner_estima_impacto_e_esforco(self):
        pedido = self.pedido("Exportar relatórios")
        estimativa = servicos.estimar(pedido=pedido, autor=self.ricardo, impacto=3, esforco=5)
        self.assertEqual((estimativa.impacto, estimativa.esforco, estimativa.relacao), (3, 5, 0.6))

    def test_programador_estima_so_o_esforco(self):
        pedido = self.pedido("Exportar relatórios")
        servicos.estimar(pedido=pedido, autor=self.diogo, esforco=3)
        with self.assertRaises(SemPermissao):
            servicos.estimar(pedido=pedido, autor=self.diogo, impacto=2)

    def test_cliente_nao_estima(self):
        with self.assertRaises(SemPermissao):
            servicos.estimar(pedido=self.pedido("Exportar relatórios"), autor=self.sofia, esforco=3)

    def test_escala_fixa(self):
        pedido = self.pedido("Exportar relatórios")
        with self.assertRaises(servicos.EstimativaInvalida):
            servicos.estimar(pedido=pedido, autor=self.ricardo, esforco=4)
        with self.assertRaises(servicos.EstimativaInvalida):
            servicos.estimar(pedido=pedido, autor=self.ricardo, impacto=5)


class Ordenar(Dados, TestCase):
    def test_so_o_product_owner_ordena(self):
        a = self.pedido("Exportar relatórios")
        with self.assertRaises(SemPermissao):
            servicos.ordenar(autor=self.marta, ids=[a.id])

    def test_a_ordem_fica_registada_com_autor_e_razao(self):
        a, b = self.pedido("Exportar relatórios"), self.pedido("Ligação ao Slack")
        servicos.ordenar(autor=self.ricardo, ids=[b.id, a.id], razao="O cliente principal pediu o Slack")
        itens, _ = servicos.lista()
        self.assertEqual([p.id for p in itens], [b.id, a.id])
        registo = AlteracaoOrdem.objects.get()
        self.assertEqual(registo.autor, self.ricardo)
        self.assertEqual(registo.razao, "O cliente principal pediu o Slack")
        self.assertEqual(registo.ordem, [b.id, a.id])

    def test_nao_ordena_pedidos_fora_da_priorizacao(self):
        novo = self.pedido("Pedido ainda novo", estado=Estado.NOVO)
        with self.assertRaises(servicos.EstimativaInvalida):
            servicos.ordenar(autor=self.ricardo, ids=[novo.id])

    def test_quem_sai_da_ordem_vai_para_o_fim(self):
        a, b = self.pedido("Exportar relatórios"), self.pedido("Ligação ao Slack")
        servicos.ordenar(autor=self.ricardo, ids=[a.id, b.id])
        servicos.ordenar(autor=self.ricardo, ids=[b.id])
        itens, _ = servicos.lista()
        self.assertEqual([(p.id, p.posicao) for p in itens], [(b.id, 1), (a.id, None)])


class Lista(Dados, TestCase):
    def test_ordena_por_impacto_esforco_e_relacao(self):
        a, b = self.pedido("Exportar relatórios"), self.pedido("Ligação ao Slack")
        servicos.estimar(pedido=a, autor=self.ricardo, impacto=3, esforco=8)
        servicos.estimar(pedido=b, autor=self.ricardo, impacto=2, esforco=2)
        self.assertEqual([p.id for p in servicos.lista("impacto")[0]], [a.id, b.id])
        self.assertEqual([p.id for p in servicos.lista("esforco")[0]], [b.id, a.id])
        self.assertEqual([p.id for p in servicos.lista("relacao")[0]], [b.id, a.id])

    def test_por_votos(self):
        a, b = self.pedido("Exportar relatórios"), self.pedido("Ligação ao Slack")
        alternar_voto(pedido=b, utilizador=self.sofia)
        self.assertEqual([p.id for p in servicos.lista("votos")[0]], [b.id, a.id])

    def test_so_entram_pedidos_em_analise_ou_aprovados(self):
        self.pedido("Ainda novo", estado=Estado.NOVO)
        em_analise = self.pedido("Em análise", estado=Estado.EM_ANALISE)
        aprovado = self.pedido("Aprovado")
        self.assertEqual({p.id for p in servicos.lista()[0]}, {em_analise.id, aprovado.id})

    def test_avisa_quando_a_ordem_passa_a_capacidade(self):
        a, b = self.pedido("Exportar relatórios"), self.pedido("Ligação ao Slack")
        servicos.estimar(pedido=a, autor=self.ricardo, esforco=8)
        servicos.estimar(pedido=b, autor=self.ricardo, esforco=8)
        servicos.ordenar(autor=self.ricardo, ids=[a.id, b.id])
        itens, aviso = servicos.lista(capacidade=10)
        self.assertIn("16 pontos", aviso)
        self.assertEqual([p.fora_da_capacidade for p in itens], [False, True])
        self.assertEqual(servicos.lista(capacidade=20)[1], "")
