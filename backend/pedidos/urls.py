from django.urls import path

from . import api

urlpatterns = [
    path("categorias/", api.CategoriaLista.as_view(), name="categorias"),
    path("etiquetas/", api.EtiquetaLista.as_view(), name="etiquetas"),
    path("pedidos/", api.PedidoLista.as_view(), name="pedidos"),
    path("pedidos/parecidos/", api.Parecidos.as_view(), name="parecidos"),
    path("pedidos/<int:pk>/", api.PedidoDetalhe.as_view(), name="pedido"),
    path("pedidos/<int:pk>/voto/", api.Votar.as_view(), name="votar"),
    path("pedidos/<int:pk>/estado/", api.MudarEstado.as_view(), name="mudar-estado"),
    path("pedidos/<int:pk>/classificar/", api.Classificar.as_view(), name="classificar"),
]
