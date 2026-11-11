from django.contrib import admin

from .models import Comentario, Notificacao, Preferencias


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ["pedido", "autor", "criado_em"]


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ["utilizador", "tipo", "texto", "lida", "criada_em"]
    list_filter = ["tipo", "lida"]


admin.site.register(Preferencias)
