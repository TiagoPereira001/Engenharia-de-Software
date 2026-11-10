from django.contrib import admin

from .models import Equipa, ItemBacklog, Sprint


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ["nome", "inicio", "fim", "capacidade", "estado"]


@admin.register(ItemBacklog)
class ItemBacklogAdmin(admin.ModelAdmin):
    list_display = ["pedido", "sprint", "equipa"]
    list_filter = ["sprint", "equipa"]


admin.site.register(Equipa)
