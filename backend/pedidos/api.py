from django.db.models import Count, Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from contas.permissoes import GerePedidos

from . import servicos
from .models import Categoria, Pedido
from .serializers import CategoriaSerializer, MudarEstadoSerializer, PedidoDetalheSerializer, PedidoSerializer


def pedidos_com_votos():
    return Pedido.objects.select_related("autor", "categoria").annotate(total_votos=Count("votos")).order_by("-criado_em", "-id")


class CategoriaLista(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    pagination_class = None


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


class PedidoDetalhe(generics.RetrieveAPIView):
    serializer_class = PedidoDetalheSerializer

    def get_queryset(self):
        return pedidos_com_votos().prefetch_related("historico__autor")


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
    permission_classes = [GerePedidos]

    def post(self, request, pk):
        pedido = generics.get_object_or_404(Pedido, pk=pk)
        entrada = MudarEstadoSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        try:
            servicos.mudar_estado(pedido=pedido, autor=request.user, **entrada.validated_data)
        except servicos.RegraViolada as erro:
            return Response({"erro": str(erro)}, status=status.HTTP_400_BAD_REQUEST)
        pedido = pedidos_com_votos().get(pk=pk)
        return Response(PedidoDetalheSerializer(pedido, context={"request": request}).data)
