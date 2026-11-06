from rest_framework import serializers

from .models import ESFORCOS, AlteracaoOrdem, Impacto


class ItemPriorizacaoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    titulo = serializers.CharField()
    estado = serializers.CharField()
    estado_nome = serializers.CharField(source="get_estado_display")
    total_votos = serializers.IntegerField()
    impacto = serializers.IntegerField(allow_null=True)
    esforco = serializers.IntegerField(allow_null=True)
    relacao = serializers.FloatField(allow_null=True)
    posicao = serializers.IntegerField(allow_null=True)
    fora_da_capacidade = serializers.BooleanField()


class EstimarSerializer(serializers.Serializer):
    impacto = serializers.ChoiceField(choices=Impacto.choices, required=False)
    esforco = serializers.ChoiceField(choices=ESFORCOS, required=False)


class OrdenarSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)
    razao = serializers.CharField(required=False, allow_blank=True, default="")
    aceitou_sugestao_ia = serializers.BooleanField(required=False, default=False)


class AlteracaoOrdemSerializer(serializers.ModelSerializer):
    autor = serializers.CharField(source="autor.username")

    class Meta:
        model = AlteracaoOrdem
        fields = ["id", "autor", "quando", "razao", "ordem", "aceitou_sugestao_ia"]
