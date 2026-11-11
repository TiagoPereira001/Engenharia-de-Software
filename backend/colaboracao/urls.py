from django.urls import path

from . import api

urlpatterns = [
    path("pedidos/<int:pedido>/comentarios/", api.Comentarios.as_view(), name="comentarios"),
    path("comentarios/<int:pk>/", api.ComentarioDetalhe.as_view(), name="comentario"),
    path("pessoas/", api.Pessoas.as_view(), name="pessoas"),
    path("notificacoes/", api.Notificacoes.as_view(), name="notificacoes"),
    path("notificacoes/lidas/", api.MarcarLidas.as_view(), name="notificacoes-lidas"),
    path("preferencias/", api.PreferenciasView.as_view(), name="preferencias"),
]
