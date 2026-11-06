from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from contas.models import Papel
from pedidos.models import Pedido
from pedidos.servicos import SemPermissao

from . import ia, servicos
from .models import ESFORCOS, AlteracaoOrdem, Impacto
from .serializers import AlteracaoOrdemSerializer, EstimarSerializer, ItemPriorizacaoSerializer, OrdenarSerializer


def capacidade_do_pedido(request):
    """Capacidade do sprint a usar no aviso. Vem no endereço ou, por omissão, das definições."""
    try:
        return int(request.query_params.get("capacidade", settings.CAPACIDADE_SPRINT))
    except ValueError:
        return settings.CAPACIDADE_SPRINT


def resposta_da_lista(request):
    capacidade = capacidade_do_pedido(request)
    itens, aviso = servicos.lista(request.query_params.get("ordem", "manual"), capacidade)
    return {
        "itens": ItemPriorizacaoSerializer(itens, many=True).data,
        "capacidade": capacidade,
        "aviso": aviso,
        "escala": {
            "impacto": [{"valor": v, "nome": n} for v, n in Impacto.choices],
            "esforco": ESFORCOS,
        },
    }


class Lista(APIView):
    """A ordem atual. Toda a equipa a vê, sem o Product Owner ter de a apresentar (US-06)."""

    permission_classes = []

    def get(self, request):
        return Response(resposta_da_lista(request))


class Estimar(APIView):
    """Impacto e esforço de um pedido (US-09)."""

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        pedido = generics.get_object_or_404(Pedido, pk=pk)
        entrada = EstimarSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        try:
            servicos.estimar(pedido=pedido, autor=request.user, **entrada.validated_data)
        except SemPermissao as erro:
            return Response({"erro": str(erro)}, status=status.HTTP_403_FORBIDDEN)
        except servicos.EstimativaInvalida as erro:
            return Response({"erro": str(erro)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(resposta_da_lista(request))


class Ordenar(APIView):
    """O Product Owner grava a ordem, com a razão (US-06)."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        entrada = OrdenarSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        try:
            servicos.ordenar(autor=request.user, **entrada.validated_data)
        except SemPermissao as erro:
            return Response({"erro": str(erro)}, status=status.HTTP_403_FORBIDDEN)
        except servicos.EstimativaInvalida as erro:
            return Response({"erro": str(erro)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(resposta_da_lista(request))


class Historico(generics.ListAPIView):
    """As últimas mudanças de ordem, com autor, data e razão."""

    permission_classes = []
    serializer_class = AlteracaoOrdemSerializer
    pagination_class = None

    def get_queryset(self):
        return AlteracaoOrdem.objects.select_related("autor")[:20]


class Sugestao(APIView):
    """Sugestão de prioridade (US-08). Só o Product Owner a pede, porque é ele que decide."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.papel != Papel.PRODUCT_OWNER:
            return Response({"erro": "Só o Product Owner pede sugestões."}, status=status.HTTP_403_FORBIDDEN)
        itens, _ = servicos.lista()
        dados = [
            {"id": p.id, "titulo": p.titulo, "votos": p.total_votos, "impacto": p.impacto, "esforco": p.esforco}
            for p in itens
        ]
        sugestoes, fonte = ia.sugerir(dados)
        titulos = {p.id: p.titulo for p in itens}
        return Response(
            {
                "fonte": fonte,
                "sugestoes": [dict(ia.como_dict(s), titulo=titulos[s.pedido_id]) for s in sugestoes],
                "ordem_sugerida": [s.pedido_id for s in sugestoes],
            }
        )
