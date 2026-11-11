from django.conf import settings
from django.db import models

from pedidos.models import Pedido


class Comentario(models.Model):
    """Conversa sobre um pedido, no sítio onde o pedido está (US-21)."""

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="comentarios")
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="comentarios")
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    editado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["criado_em", "id"]


class TipoNotificacao(models.TextChoices):
    ESTADO = "estado", "Mudança de estado"
    MENCAO = "mencao", "Menção"
    COMENTARIO = "comentario", "Comentário"


class Notificacao(models.Model):
    """Aviso curto: diz o pedido e o que aconteceu (US-22, US-23)."""

    utilizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notificacoes")
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True, blank=True, related_name="+")
    tipo = models.CharField(max_length=12, choices=TipoNotificacao.choices)
    texto = models.CharField(max_length=200)
    criada_em = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    class Meta:
        ordering = ["-criada_em", "-id"]


class Preferencias(models.Model):
    """O que cada pessoa quer receber (US-22). Por omissão, tudo no sistema e nada por email."""

    utilizador = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preferencias")
    estados = models.BooleanField(default=True, help_text="Muda o estado de um pedido que sigo.")
    mencoes = models.BooleanField(default=True, help_text="Alguém me menciona.")
    comentarios = models.BooleanField(default=True, help_text="Há comentários novos em pedidos que sigo.")
    email = models.BooleanField(default=False, help_text="Também por email.")

    QUER = {
        TipoNotificacao.ESTADO: "estados",
        TipoNotificacao.MENCAO: "mencoes",
        TipoNotificacao.COMENTARIO: "comentarios",
    }

    def quer(self, tipo):
        return getattr(self, self.QUER[tipo])
