from django.urls import path

from . import api

urlpatterns = [
    path("eu/", api.EuView.as_view(), name="eu"),
    path("registar/", api.RegistarView.as_view(), name="registar"),
    path("entrar/", api.EntrarView.as_view(), name="entrar"),
    path("sair/", api.SairView.as_view(), name="sair"),
]
