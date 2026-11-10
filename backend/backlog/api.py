from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pedidos.models import Pedido
from pedidos.servicos import RegraViolada, SemPermissao

from . import servicos
from .models import Equipa, ItemBacklog, Sprint
from .serializers import (
    AtribuirEquipaSerializer,
    EquipaSerializer,
    ItemSerializer,
    PedidoSerializer,
    SprintSerializer,
)


def erro(falha):
    codigo = status.HTTP_403_FORBIDDEN if isinstance(falha, SemPermissao) else status.HTTP_400_BAD_REQUEST
    return Response({"erro": str(falha)}, status=codigo)


def itens(lista, request):
    return ItemSerializer(lista, many=True, context={"request": request}).data


class EquipaLista(generics.ListAPIView):
    permission_classes = []
    queryset = Equipa.objects.all()
    serializer_class = EquipaSerializer
    pagination_class = None


class ProductBacklog(APIView):
    """O product backlog, pela ordem do Product Owner, e acrescentar pedidos aprovados (US-10)."""

    def get(self, request):
        return Response({"itens": itens(servicos.product_backlog(), request)})

    def post(self, request):
        entrada = PedidoSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        pedido = generics.get_object_or_404(Pedido, pk=entrada.validated_data["pedido"])
        try:
            servicos.acrescentar_ao_backlog(pedido=pedido, autor=request.user)
        except (SemPermissao, RegraViolada) as falha:
            return erro(falha)
        return Response({"itens": itens(servicos.product_backlog(), request)}, status=status.HTTP_201_CREATED)


class AtribuirEquipa(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pedido):
        item = generics.get_object_or_404(ItemBacklog, pedido_id=pedido)
        entrada = AtribuirEquipaSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        try:
            servicos.atribuir_equipa(item=item, autor=request.user, equipa=entrada.validated_data["equipa"])
        except SemPermissao as falha:
            return erro(falha)
        return Response(ItemSerializer(item, context={"request": request}).data)


class SprintLista(generics.ListAPIView):
    """Os sprints que ainda não fecharam, e criar um sprint novo (US-11)."""

    serializer_class = SprintSerializer
    pagination_class = None

    def get_queryset(self):
        return Sprint.objects.exclude(estado="fechado")

    def post(self, request):
        entrada = SprintSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        try:
            sprint = servicos.criar_sprint(autor=request.user, **entrada.validated_data)
        except (SemPermissao, RegraViolada) as falha:
            return erro(falha)
        return Response(SprintSerializer(sprint).data, status=status.HTTP_201_CREATED)


def detalhe_do_sprint(sprint, request):
    dados = SprintSerializer(sprint).data
    dados["itens"] = itens(sprint.itens.select_related("pedido__estimativa", "equipa"), request)
    return dados


class SprintDetalhe(APIView):
    def get(self, request, pk):
        return Response(detalhe_do_sprint(generics.get_object_or_404(Sprint, pk=pk), request))


class ItensDoSprint(APIView):
    """Pôr um item do product backlog no sprint, ou tirá-lo."""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        sprint = generics.get_object_or_404(Sprint, pk=pk)
        entrada = PedidoSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        item = generics.get_object_or_404(ItemBacklog, pedido_id=entrada.validated_data["pedido"])
        try:
            servicos.por_no_sprint(item=item, sprint=sprint, autor=request.user)
        except (SemPermissao, RegraViolada) as falha:
            return erro(falha)
        return Response(detalhe_do_sprint(sprint, request))

    def delete(self, request, pk, pedido):
        sprint = generics.get_object_or_404(Sprint, pk=pk)
        item = generics.get_object_or_404(ItemBacklog, pedido_id=pedido, sprint=sprint)
        try:
            servicos.tirar_do_sprint(item=item, autor=request.user)
        except SemPermissao as falha:
            return erro(falha)
        return Response(detalhe_do_sprint(sprint, request))


class ComecarSprint(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        sprint = generics.get_object_or_404(Sprint, pk=pk)
        try:
            servicos.comecar_sprint(sprint=sprint, autor=request.user)
        except (SemPermissao, RegraViolada) as falha:
            return erro(falha)
        return Response(detalhe_do_sprint(sprint, request))


class FecharSprint(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        sprint = generics.get_object_or_404(Sprint, pk=pk)
        try:
            voltaram = servicos.fechar_sprint(sprint=sprint, autor=request.user)
        except (SemPermissao, RegraViolada) as falha:
            return erro(falha)
        return Response({"voltaram_ao_backlog": voltaram, "sprint": SprintSerializer(sprint).data})


class Quadro(APIView):
    """Quadro do sprint (ecrã 07): uma coluna por estado, com filtro por equipa."""

    def get(self, request, pk):
        sprint = generics.get_object_or_404(Sprint, pk=pk)
        colunas = servicos.quadro(sprint, request.query_params.get("equipa"))
        return Response(
            {
                "sprint": SprintSerializer(sprint).data,
                "colunas": [
                    {"estado": estado, "nome": estado.label, "itens": itens(lista, request)}
                    for estado, lista in colunas.items()
                ],
            }
        )
