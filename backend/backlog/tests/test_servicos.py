"""Testes às regras do backlog e dos sprints (US-10, US-11 e US-13)."""

from datetime import date

from django.test import TestCase

from backlog import servicos
from backlog.models import EstadoSprint
from pedidos import servicos as pedidos
from pedidos.models import Estado
from pedidos.servicos import RegraViolada, SemPermissao
from priorizacao import servicos as priorizacao

from .base import Dados


class ProductBacklog(Dados, TestCase):
    def test_so_entram_pedidos_aprovados(self):
        novo = pedidos.criar_pedido(autor=self.sofia, titulo="Ainda novo", descricao="x", categoria=self.cat)
        with self.assertRaises(RegraViolada):
            servicos.acrescentar_ao_backlog(pedido=novo, autor=self.ricardo)

    def test_so_o_product_owner_acrescenta(self):
        with self.assertRaises(SemPermissao):
            servicos.acrescentar_ao_backlog(pedido=self.aprovado("Exportar"), autor=self.marta)

    def test_segue_a_ordem_do_product_owner(self):
        a, b = self.no_backlog("Exportar relatórios"), self.no_backlog("Ligação ao Slack")
        priorizacao.ordenar(autor=self.ricardo, ids=[b.pedido_id, a.pedido_id])
        self.assertEqual([i.pedido_id for i in servicos.product_backlog()], [b.pedido_id, a.pedido_id])


class Sprint(Dados, TestCase):
    def test_sprint_tem_datas_e_objetivo(self):
        dia_9, dia_20 = date(2026, 11, 9), date(2026, 11, 20)
        with self.assertRaises(RegraViolada):
            servicos.criar_sprint(autor=self.ricardo, nome="S", objetivo="x", inicio=dia_20, fim=dia_9, capacidade=10)
        with self.assertRaises(RegraViolada):
            servicos.criar_sprint(autor=self.ricardo, nome="S", objetivo=" ", inicio=dia_9, fim=dia_20, capacidade=10)

    def test_sem_estimativa_nao_entra_no_sprint(self):
        item = self.no_backlog("Exportar relatórios")
        with self.assertRaises(RegraViolada):
            servicos.por_no_sprint(item=item, sprint=self.sprint(), autor=self.ricardo)

    def test_avisa_quando_passa_a_capacidade(self):
        sprint = self.sprint(capacidade=10)
        self.assertEqual(servicos.por_no_sprint(item=self.no_backlog("A", 8), sprint=sprint, autor=self.ricardo), "")
        aviso = servicos.por_no_sprint(item=self.no_backlog("B", 5), sprint=sprint, autor=self.ricardo)
        self.assertIn("13 pontos", aviso)
        self.assertEqual(servicos.product_backlog(), [])

    def test_o_que_nao_acaba_volta_ao_backlog(self):
        sprint = self.sprint()
        feito, por_fazer = self.no_backlog("Feito", 3), self.no_backlog("Por fazer", 3)
        for item in (feito, por_fazer):
            servicos.por_no_sprint(item=item, sprint=sprint, autor=self.ricardo)
        servicos.comecar_sprint(sprint=sprint, autor=self.ricardo)
        pedido = feito.pedido
        pedidos.mudar_estado(pedido=pedido, para=Estado.EM_DESENVOLVIMENTO, autor=self.diogo)
        pedidos.mudar_estado(pedido=pedido, para=Estado.EM_REVISAO, autor=self.diogo)
        pedidos.mudar_estado(pedido=pedido, para=Estado.CONCLUIDO, autor=self.ricardo)
        self.assertEqual(servicos.fechar_sprint(sprint=sprint, autor=self.ricardo), 1)
        self.assertEqual(sprint.estado, EstadoSprint.FECHADO)
        self.assertEqual([i.pedido_id for i in servicos.product_backlog()], [por_fazer.pedido_id])

    def test_so_um_sprint_em_curso(self):
        primeiro, segundo = self.sprint(), self.sprint()
        servicos.comecar_sprint(sprint=primeiro, autor=self.ricardo)
        with self.assertRaises(RegraViolada):
            servicos.comecar_sprint(sprint=segundo, autor=self.ricardo)

    def test_quadro_tem_uma_coluna_por_estado_e_filtra_por_equipa(self):
        sprint = self.sprint()
        com_equipa, sem_equipa = self.no_backlog("A", 3), self.no_backlog("B", 3)
        for item in (com_equipa, sem_equipa):
            servicos.por_no_sprint(item=item, sprint=sprint, autor=self.ricardo)
        servicos.atribuir_equipa(item=com_equipa, equipa=self.equipa, autor=self.helena)
        colunas = servicos.quadro(sprint)
        self.assertEqual([e.label for e in colunas], ["Aprovado", "Em desenvolvimento", "Em revisão", "Concluído"])
        self.assertEqual(len(colunas[Estado.APROVADO]), 2)
        da_equipa = servicos.quadro(sprint, self.equipa.id)[Estado.APROVADO]
        self.assertEqual([i.pedido_id for i in da_equipa], [com_equipa.pedido_id])


class Equipas(Dados, TestCase):
    def test_gestor_de_projeto_atribui_e_cliente_nao(self):
        item = self.no_backlog("Exportar relatórios")
        servicos.atribuir_equipa(item=item, equipa=self.equipa, autor=self.helena)
        self.assertEqual(item.equipa, self.equipa)
        with self.assertRaises(SemPermissao):
            servicos.atribuir_equipa(item=item, equipa=None, autor=self.sofia)
