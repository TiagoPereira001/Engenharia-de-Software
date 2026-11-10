from django.urls import path

from . import api

urlpatterns = [
    path("", api.ProductBacklog.as_view(), name="backlog"),
    path("equipas/", api.EquipaLista.as_view(), name="equipas"),
    path("<int:pedido>/equipa/", api.AtribuirEquipa.as_view(), name="atribuir-equipa"),
    path("sprints/", api.SprintLista.as_view(), name="sprints"),
    path("sprints/<int:pk>/", api.SprintDetalhe.as_view(), name="sprint"),
    path("sprints/<int:pk>/itens/", api.ItensDoSprint.as_view(), name="sprint-itens"),
    path("sprints/<int:pk>/itens/<int:pedido>/", api.ItensDoSprint.as_view(), name="sprint-item"),
    path("sprints/<int:pk>/comecar/", api.ComecarSprint.as_view(), name="sprint-comecar"),
    path("sprints/<int:pk>/fechar/", api.FecharSprint.as_view(), name="sprint-fechar"),
    path("sprints/<int:pk>/quadro/", api.Quadro.as_view(), name="sprint-quadro"),
]
