"""Testes aos comentários, menções e notificações (US-21, US-22 e US-23)."""

from django.core import mail
from django.test import TestCase

from colaboracao import servicos
from colaboracao.models import Notificacao, TipoNotificacao
from pedidos import servicos as pedidos
from pedidos.models import Estado
from pedidos.servicos import RegraViolada, SemPermissao

from .base import Dados


class Comentarios(Dados, TestCase):
    def test_comentario_tem_autor_e_data(self):
        comentario = servicos.comentar(pedido=self.pedido, autor=self.ricardo, texto="  Que colunas precisas?  ")
        self.assertEqual((comentario.autor, comentario.texto), (self.ricardo, "Que colunas precisas?"))
        self.assertIsNotNone(comentario.criado_em)

    def test_comentario_vazio_nao_entra(self):
        with self.assertRaises(RegraViolada):
            servicos.comentar(pedido=self.pedido, autor=self.ricardo, texto="   ")

    def test_so_o_autor_edita_e_apaga(self):
        comentario = servicos.comentar(pedido=self.pedido, autor=self.ricardo, texto="Primeira versão")
        with self.assertRaises(SemPermissao):
            servicos.editar(comentario=comentario, autor=self.diogo, texto="Outra coisa")
        servicos.editar(comentario=comentario, autor=self.ricardo, texto="Segunda versão")
        self.assertIsNotNone(comentario.editado_em)
        with self.assertRaises(SemPermissao):
            servicos.apagar(comentario=comentario, autor=self.sofia)
        servicos.apagar(comentario=comentario, autor=self.ricardo)
        self.assertFalse(self.pedido.comentarios.exists())


class Notificacoes(Dados, TestCase):
    def test_quem_pediu_e_avisado_quando_o_estado_muda(self):
        pedidos.mudar_estado(pedido=self.pedido, para=Estado.EM_ANALISE, autor=self.marta)
        aviso = Notificacao.objects.get(utilizador=self.sofia)
        self.assertEqual(aviso.tipo, TipoNotificacao.ESTADO)
        self.assertEqual(aviso.texto, "«Exportar relatórios» passou a Em análise")
        self.assertFalse(Notificacao.objects.filter(utilizador=self.marta).exists())

    def test_quem_votou_tambem_segue_o_pedido(self):
        pedidos.alternar_voto(pedido=self.pedido, utilizador=self.diogo)
        pedidos.mudar_estado(pedido=self.pedido, para=Estado.EM_ANALISE, autor=self.marta)
        self.assertTrue(Notificacao.objects.filter(utilizador=self.diogo, tipo=TipoNotificacao.ESTADO).exists())

    def test_rejeitado_leva_o_motivo(self):
        pedidos.mudar_estado(pedido=self.pedido, para=Estado.EM_ANALISE, autor=self.marta)
        pedidos.mudar_estado(pedido=self.pedido, para=Estado.REJEITADO, autor=self.marta, motivo="Repetido")
        self.assertIn("Motivo: Repetido", Notificacao.objects.filter(utilizador=self.sofia).first().texto)

    def test_mencao_avisa_a_pessoa_uma_vez(self):
        servicos.comentar(pedido=self.pedido, autor=self.diogo, texto="@sofia o total por mês chega?")
        avisos = Notificacao.objects.filter(utilizador=self.sofia)
        self.assertEqual([a.tipo for a in avisos], [TipoNotificacao.MENCAO])
        self.assertEqual(avisos[0].texto, "diogo mencionou-te em «Exportar relatórios»")

    def test_comentario_avisa_quem_segue_menos_quem_escreveu(self):
        servicos.comentar(pedido=self.pedido, autor=self.ricardo, texto="Que colunas precisas?")
        self.assertEqual(Notificacao.objects.filter(utilizador=self.sofia, tipo=TipoNotificacao.COMENTARIO).count(), 1)
        self.assertFalse(Notificacao.objects.filter(utilizador=self.ricardo).exists())

    def test_preferencias_escolhem_o_que_chega(self):
        prefs = servicos.preferencias(self.sofia)
        prefs.estados = False
        prefs.save()
        pedidos.mudar_estado(pedido=self.pedido, para=Estado.EM_ANALISE, autor=self.marta)
        self.assertFalse(Notificacao.objects.filter(utilizador=self.sofia).exists())

    def test_tambem_por_email_se_a_pessoa_quiser(self):
        prefs = servicos.preferencias(self.sofia)
        prefs.email = True
        prefs.save()
        pedidos.mudar_estado(pedido=self.pedido, para=Estado.EM_ANALISE, autor=self.marta)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("passou a Em análise", mail.outbox[0].body)

    def test_marcar_lidas(self):
        pedidos.mudar_estado(pedido=self.pedido, para=Estado.EM_ANALISE, autor=self.marta)
        pedidos.mudar_estado(pedido=self.pedido, para=Estado.APROVADO, autor=self.marta)
        primeira = Notificacao.objects.filter(utilizador=self.sofia).last()
        self.assertEqual(servicos.marcar_lidas(utilizador=self.sofia, ids=[primeira.id]), 1)
        self.assertEqual(servicos.marcar_lidas(utilizador=self.sofia), 1)
