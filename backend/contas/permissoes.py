from rest_framework.permissions import BasePermission


class GerePedidos(BasePermission):
    """Só o product manager e o Product Owner mudam o estado de um pedido."""

    message = "Só o product manager ou o Product Owner podem fazer isto."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.gere_pedidos)
