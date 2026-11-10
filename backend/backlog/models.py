from django.db import models

from pedidos.models import Pedido


class Equipa(models.Model):
    """Equipa de desenvolvimento a quem se atribui trabalho (US-13)."""

    nome = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class EstadoSprint(models.TextChoices):
    PLANEADO = "planeado", "Planeado"
    EM_CURSO = "em_curso", "Em curso"
    FECHADO = "fechado", "Fechado"


class Sprint(models.Model):
    """Um sprint tem datas, objetivo e capacidade em pontos (US-11)."""

    nome = models.CharField(max_length=60)
    objetivo = models.TextField()
    inicio = models.DateField()
    fim = models.DateField()
    capacidade = models.PositiveIntegerField(help_text="Pontos que a equipa consegue fazer neste sprint.")
    estado = models.CharField(max_length=10, choices=EstadoSprint.choices, default=EstadoSprint.PLANEADO)

    class Meta:
        ordering = ["inicio", "id"]

    def __str__(self):
        return self.nome


class ItemBacklog(models.Model):
    """Um pedido aprovado que entrou no product backlog (US-10).

    Sem sprint, está no product backlog; com sprint, está no sprint backlog (US-11).
    """

    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name="item_backlog")
    sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL, null=True, blank=True, related_name="itens")
    equipa = models.ForeignKey(Equipa, on_delete=models.SET_NULL, null=True, blank=True, related_name="itens")
    acrescentado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pedido)
