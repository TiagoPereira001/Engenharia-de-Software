from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistoSerializer, UtilizadorSerializer


@method_decorator(ensure_csrf_cookie, name="dispatch")
class EuView(APIView):
    """Diz quem está a usar o sistema. Também entrega o cookie de CSRF ao front-end."""

    permission_classes = [AllowAny]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"autenticado": False})
        return Response({"autenticado": True, "utilizador": UtilizadorSerializer(request.user).data})


class RegistarView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        utilizador = serializer.save()
        login(request, utilizador)
        return Response(UtilizadorSerializer(utilizador).data, status=status.HTTP_201_CREATED)


class EntrarView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        utilizador = authenticate(
            request,
            username=request.data.get("username", ""),
            password=request.data.get("password", ""),
        )
        if utilizador is None:
            # A mesma mensagem para utilizador inexistente e palavra-passe errada.
            return Response({"erro": "Utilizador ou palavra-passe errados."}, status=status.HTTP_400_BAD_REQUEST)
        login(request, utilizador)
        return Response(UtilizadorSerializer(utilizador).data)


class SairView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
