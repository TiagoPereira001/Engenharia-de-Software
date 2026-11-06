from django.contrib import admin

from .models import AlteracaoOrdem, Estimativa


@admin.register(Estimativa)
class EstimativaAdmin(admin.ModelAdmin):
    list_display = ["pedido", "impacto", "esforco", "posicao"]


@admin.register(AlteracaoOrdem)
class AlteracaoOrdemAdmin(admin.ModelAdmin):
    list_display = ["quando", "autor", "razao", "aceitou_sugestao_ia"]
