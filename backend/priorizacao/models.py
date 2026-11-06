from django.conf import settings
from django.db import models

from pedidos.models import Pedido


class Impacto(models.IntegerChoices):
    """Escala fixa do impacto (US-09). Baixo, médio ou alto para o produto."""

    BAIXO = 1, "Baixo"
    MEDIO = 2, "Médio"
    ALTO = 3, "Alto"


# Esforço em pontos, a mesma escala que a equipa usa no Jira (Fibonacci).
ESFORCOS = [1, 2, 3, 5, 8, 13]


class Estimativa(models.Model):
    """O que o Product Owner sabe de cada pedido para o priorizar: impacto, esforço e lugar na ordem."""

    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name="estimativa")
    impacto = models.PositiveSmallIntegerField(choices=Impacto.choices, null=True, blank=True)
    esforco = models.PositiveSmallIntegerField(choices=[(p, f"{p} pontos") for p in ESFORCOS], null=True, blank=True)
    # Lugar na ordem do Product Owner (1 é o primeiro). Vazio enquanto ninguém o ordenou.
    posicao = models.PositiveIntegerField(null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pedido} (impacto {self.impacto}, esforço {self.esforco})"

    @property
    def relacao(self):
        """Impacto por ponto de esforço: quanto maior, mais vale fazer primeiro."""
        if not self.impacto or not self.esforco:
            return None
        return round(self.impacto / self.esforco, 2)


class AlteracaoOrdem(models.Model):
    """Cada vez que o Product Owner muda a ordem fica aqui, com data, autor e razão (US-06)."""

    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    quando = models.DateTimeField(auto_now_add=True)
    razao = models.TextField(blank=True)
    # Os ids dos pedidos pela ordem que ficou.
    ordem = models.JSONField(default=list)
    aceitou_sugestao_ia = models.BooleanField(default=False)

    class Meta:
        ordering = ["-quando", "-id"]
