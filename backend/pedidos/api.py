from django.db.models import Count, Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import servicos
from .models import Categoria, Etiqueta, Pedido
from .serializers import (
    CategoriaSerializer,
    ClassificarSerializer,
    MudarEstadoSerializer,
    PedidoDetalheSerializer,
    PedidoSerializer,
)


def pedidos_com_votos():
    return (
        Pedido.objects.select_related("autor", "categoria")
        .prefetch_related("etiquetas")
        .annotate(total_votos=Count("votos"))
        .order_by("-criado_em", "-id")
    )


def detalhe(pk, request):
    pedido = pedidos_com_votos().prefetch_related("historico__autor").get(pk=pk)
    return PedidoDetalheSerializer(pedido, context={"request": request}).data


class CategoriaLista(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    pagination_class = None


class EtiquetaLista(APIView):
    permission_classes = []

    def get(self, request):
        return Response(list(Etiqueta.objects.values_list("nome", flat=True)))


class PedidoLista(generics.ListCreateAPIView):
    """Lista com pesquisa e filtros (US-04) e criação de pedidos (US-01)."""

    serializer_class = PedidoSerializer

    def get_queryset(self):
        qs = pedidos_com_votos()
        q = self.request.query_params.get("q", "").strip()
        if q:
            qs = qs.filter(Q(titulo__icontains=q) | Q(descricao__icontains=q))
        if estado := self.request.query_params.get("estado"):
            qs = qs.filter(estado=estado)
        if categoria := self.request.query_params.get("categoria"):
            qs = qs.filter(categoria_id=categoria)
        if etiqueta := self.request.query_params.get("etiqueta"):
            qs = qs.filter(etiquetas__nome=etiqueta.strip().lower())
        # "Os meus pedidos": o cliente vê tudo o que pediu e o estado de cada um (US-01).
        if self.request.query_params.get("meus") and self.request.user.is_authenticated:
            qs = qs.filter(autor=self.request.user)
        if self.request.query_params.get("ordem") == "votos":
            qs = qs.order_by("-total_votos", "-criado_em")
        return qs

    def perform_create(self, serializer):
        dados = serializer.validated_data
        pedido = servicos.criar_pedido(
            autor=self.request.user,
            titulo=dados["titulo"],
            descricao=dados["descricao"],
            categoria=dados["categoria"],
            origem=dados.get("origem", "sistema"),
        )
        serializer.instance = pedidos_com_votos().get(pk=pedido.pk)


class PedidoDetalhe(APIView):
    permission_classes = []

    def get(self, request, pk):
        generics.get_object_or_404(Pedido, pk=pk)
        return Response(detalhe(pk, request))


class Parecidos(APIView):
    """Aviso de pedidos parecidos enquanto se escreve o título (US-05)."""

    permission_classes = []

    def get(self, request):
        encontrados = servicos.procurar_parecidos(request.query_params.get("q", ""))
        dados = PedidoSerializer(encontrados, many=True, context={"request": request}).data
        return Response(dados)


class Votar(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        pedido = generics.get_object_or_404(Pedido, pk=pk)
        votei = servicos.alternar_voto(pedido=pedido, utilizador=request.user)
        return Response({"votei": votei, "total_votos": pedido.votos.count()})


class MudarEstado(APIView):
    """Quem pode fazer cada passagem está em servicos.QUEM_PODE."""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        pedido = generics.get_object_or_404(Pedido, pk=pk)
        entrada = MudarEstadoSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        try:
            servicos.mudar_estado(pedido=pedido, autor=request.user, **entrada.validated_data)
        except servicos.SemPermissao as erro:
            return Response({"erro": str(erro)}, status=status.HTTP_403_FORBIDDEN)
        except servicos.RegraViolada as erro:
            return Response({"erro": str(erro)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(detalhe(pk, request))


class Classificar(APIView):
    """Categoria e etiquetas de um pedido (US-02)."""

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        pedido = generics.get_object_or_404(Pedido, pk=pk)
        entrada = ClassificarSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        try:
            servicos.classificar(pedido=pedido, autor=request.user, **entrada.validated_data)
        except servicos.SemPermissao as erro:
            return Response({"erro": str(erro)}, status=status.HTTP_403_FORBIDDEN)
        return Response(detalhe(pk, request))
