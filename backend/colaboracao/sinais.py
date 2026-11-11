"""Avisa quem segue um pedido quando o estado dele muda (US-12 e US-22)."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from pedidos.models import Estado, MudancaEstado

from . import servicos
from .models import TipoNotificacao


@receiver(post_save, sender=MudancaEstado, dispatch_uid="colaboracao_avisa_mudanca_de_estado")
def avisar_mudanca_de_estado(sender, instance, created, **kwargs):
    # A primeira linha do histórico (o pedido a nascer Novo) não é uma mudança.
    if not created or not instance.de:
        return
    pedido = instance.pedido
    texto = f"«{pedido.titulo}» passou a {Estado(instance.para).label}"
    if instance.motivo:
        texto += f". Motivo: {instance.motivo}"
    servicos.notificar(
        utilizadores=servicos.seguidores(pedido),
        pedido=pedido,
        tipo=TipoNotificacao.ESTADO,
        texto=texto,
        exceto=instance.autor,
    )
