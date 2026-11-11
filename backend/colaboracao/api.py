from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pedidos.models import Pedido
from pedidos.servicos import RegraViolada, SemPermissao

from . import servicos
from .models import Comentario, Notificacao
from .serializers import ComentarioSerializer, LidasSerializer, NotificacaoSerializer, PreferenciasSerializer


def erro(falha):
    codigo = status.HTTP_403_FORBIDDEN if isinstance(falha, SemPermissao) else status.HTTP_400_BAD_REQUEST
    return Response({"erro": str(falha)}, status=codigo)


class Comentarios(APIView):
    """A conversa de um pedido (US-21). Ler é para todos; escrever, para quem tem conta."""

    def get(self, request, pedido):
        comentarios = Comentario.objects.filter(pedido_id=pedido).select_related("autor")
        return Response(ComentarioSerializer(comentarios, many=True, context={"request": request}).data)

    def post(self, request, pedido):
        alvo = generics.get_object_or_404(Pedido, pk=pedido)
        try:
            comentario = servicos.comentar(pedido=alvo, autor=request.user, texto=request.data.get("texto", ""))
        except RegraViolada as falha:
            return erro(falha)
        dados = ComentarioSerializer(comentario, context={"request": request}).data
        return Response(dados, status=status.HTTP_201_CREATED)


class ComentarioDetalhe(APIView):
    """Só o autor edita ou apaga o seu comentário."""

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        comentario = generics.get_object_or_404(Comentario, pk=pk)
        try:
            servicos.editar(comentario=comentario, autor=request.user, texto=request.data.get("texto", ""))
        except (SemPermissao, RegraViolada) as falha:
            return erro(falha)
        return Response(ComentarioSerializer(comentario, context={"request": request}).data)

    def delete(self, request, pk):
        comentario = generics.get_object_or_404(Comentario, pk=pk)
        try:
            servicos.apagar(comentario=comentario, autor=request.user)
        except SemPermissao as falha:
            return erro(falha)
        return Response(status=status.HTTP_204_NO_CONTENT)


class Pessoas(APIView):
    """Nomes para as menções com @ (US-23)."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        nomes = get_user_model().objects.filter(is_active=True).order_by("username").values_list("username", flat=True)
        return Response(list(nomes))


class Notificacoes(APIView):
    """As notificações de quem está autenticado, as mais recentes primeiro (US-22)."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        minhas = Notificacao.objects.filter(utilizador=request.user)
        return Response(
            {
                "por_ler": minhas.filter(lida=False).count(),
                "itens": NotificacaoSerializer(minhas[:50], many=True).data,
            }
        )


class MarcarLidas(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        entrada = LidasSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        servicos.marcar_lidas(utilizador=request.user, ids=entrada.validated_data["ids"])
        return Notificacoes().get(request)


class PreferenciasView(APIView):
    """O que cada um quer receber (US-22)."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(PreferenciasSerializer(servicos.preferencias(request.user)).data)

    def put(self, request):
        entrada = PreferenciasSerializer(servicos.preferencias(request.user), data=request.data)
        entrada.is_valid(raise_exception=True)
        entrada.save()
        return Response(entrada.data)
