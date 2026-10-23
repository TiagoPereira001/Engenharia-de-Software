from django.contrib import admin

from .models import Categoria, MudancaEstado, Pedido, Voto


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ["titulo", "categoria", "estado", "origem", "autor", "criado_em"]
    list_filter = ["estado", "categoria", "origem"]
    search_fields = ["titulo", "descricao"]


admin.site.register(Categoria)
admin.site.register(Voto)
admin.site.register(MudancaEstado)
