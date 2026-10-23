from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def saude(request):
    """Para confirmar que o servidor está a correr."""
    return JsonResponse({"ok": True})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/saude/", saude),
    path("api/contas/", include("contas.urls")),
    path("api/", include("pedidos.urls")),
]
