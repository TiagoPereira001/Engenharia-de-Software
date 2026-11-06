from django.urls import path

from . import api

urlpatterns = [
    path("", api.Lista.as_view(), name="priorizacao"),
    path("ordem/", api.Ordenar.as_view(), name="priorizacao-ordem"),
    path("historico/", api.Historico.as_view(), name="priorizacao-historico"),
    path("sugestao/", api.Sugestao.as_view(), name="priorizacao-sugestao"),
    path("<int:pk>/estimativa/", api.Estimar.as_view(), name="priorizacao-estimativa"),
]
