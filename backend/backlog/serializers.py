from rest_framework import serializers

from pedidos import servicos as regras_pedidos

from . import servicos
from .models import Equipa, Sprint


class EquipaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipa
        fields = ["id", "nome"]


class ItemSerializer(serializers.Serializer):
    """Um cartão do backlog ou do quadro: o pedido, o esforço, a equipa e o que se pode fazer com ele."""

    pedido = serializers.IntegerField(source="pedido.id")
    titulo = serializers.CharField(source="pedido.titulo")
    estado = serializers.CharField(source="pedido.estado")
    estado_nome = serializers.CharField(source="pedido.get_estado_display")
    esforco = serializers.SerializerMethodField()
    equipa = EquipaSerializer(allow_null=True)
    pronto = serializers.SerializerMethodField()
    motivo = serializers.SerializerMethodField()
    pode_mudar_para = serializers.SerializerMethodField()

    def get_esforco(self, item):
        return servicos.esforco_de(item)

    def get_pronto(self, item):
        return servicos.pronto_para_sprint(item)[0]

    def get_motivo(self, item):
        return servicos.pronto_para_sprint(item)[1]

    def get_pode_mudar_para(self, item):
        return regras_pedidos.estados_seguintes(item.pedido, self.context["request"].user)


class SprintSerializer(serializers.ModelSerializer):
    pontos = serializers.SerializerMethodField()
    aviso = serializers.SerializerMethodField()
    estado_nome = serializers.CharField(source="get_estado_display", read_only=True)

    class Meta:
        model = Sprint
        fields = ["id", "nome", "objetivo", "inicio", "fim", "capacidade", "estado", "estado_nome", "pontos", "aviso"]
        read_only_fields = ["estado"]

    def get_pontos(self, sprint):
        return servicos.pontos(sprint)

    def get_aviso(self, sprint):
        return servicos.aviso_capacidade(sprint)


class PedidoSerializer(serializers.Serializer):
    pedido = serializers.IntegerField()


class AtribuirEquipaSerializer(serializers.Serializer):
    equipa = serializers.PrimaryKeyRelatedField(queryset=Equipa.objects.all(), allow_null=True)
