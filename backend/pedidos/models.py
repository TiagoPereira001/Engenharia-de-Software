from django.conf import settings
from django.db import models


class Estado(models.TextChoices):
    """Estados de um pedido, os da US-12 (EDS-120)."""

    NOVO = "novo", "Novo"
    EM_ANALISE = "em_analise", "Em análise"
    APROVADO = "aprovado", "Aprovado"
    REJEITADO = "rejeitado", "Rejeitado"
    EM_DESENVOLVIMENTO = "em_desenvolvimento", "Em desenvolvimento"
    EM_REVISAO = "em_revisao", "Em revisão"
    CONCLUIDO = "concluido", "Concluído"


class Origem(models.TextChoices):
    """Por onde chegou o pedido. Quem regista em nome de alguém indica a origem."""

    SISTEMA = "sistema", "Sistema"
    EMAIL = "email", "Email"
    REUNIAO = "reuniao", "Reunião"
    CHAT = "chat", "Chat"


class Categoria(models.Model):
    nome = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    titulo = models.CharField(max_length=120)
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="pedidos")
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.NOVO)
    origem = models.CharField(max_length=10, choices=Origem.choices, default=Origem.SISTEMA)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="pedidos")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return self.titulo


class Voto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="votos")
    utilizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votos")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Um voto por pessoa e por pedido, garantido na base de dados (US-07).
        constraints = [models.UniqueConstraint(fields=["pedido", "utilizador"], name="um_voto_por_pessoa")]


class MudancaEstado(models.Model):
    """Histórico de estados. Serve a rastreabilidade e, mais tarde, as métricas."""

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="historico")
    de = models.CharField(max_length=20, choices=Estado.choices, blank=True)
    para = models.CharField(max_length=20, choices=Estado.choices)
    motivo = models.TextField(blank=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    quando = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["quando", "id"]
