from rest_framework import serializers

from .models import Categoria, Estado, MudancaEstado, Origem, Pedido


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nome"]


class MudancaEstadoSerializer(serializers.ModelSerializer):
    autor = serializers.CharField(source="autor.username")

    class Meta:
        model = MudancaEstado
        fields = ["de", "para", "motivo", "autor", "quando"]


class PedidoSerializer(serializers.ModelSerializer):
    autor = serializers.CharField(source="autor.username", read_only=True)
    categoria_nome = serializers.CharField(source="categoria.nome", read_only=True)
    estado_nome = serializers.CharField(source="get_estado_display", read_only=True)
    # Só o total; quem votou nunca sai da API (pedido da Sofia, US-07).
    total_votos = serializers.IntegerField(read_only=True)
    votei = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = [
            "id", "titulo", "descricao", "categoria", "categoria_nome", "estado", "estado_nome",
            "origem", "autor", "criado_em", "total_votos", "votei",
        ]
        read_only_fields = ["estado"]

    def get_votei(self, pedido):
        utilizador = self.context["request"].user
        return utilizador.is_authenticated and pedido.votos.filter(utilizador=utilizador).exists()

    def validate_titulo(self, valor):
        if len(valor.strip()) < 5:
            raise serializers.ValidationError("O título precisa de pelo menos 5 caracteres.")
        return valor


class PedidoDetalheSerializer(PedidoSerializer):
    historico = MudancaEstadoSerializer(many=True, read_only=True)

    class Meta(PedidoSerializer.Meta):
        fields = PedidoSerializer.Meta.fields + ["historico"]


class MudarEstadoSerializer(serializers.Serializer):
    para = serializers.ChoiceField(choices=Estado.choices)
    motivo = serializers.CharField(required=False, allow_blank=True, default="")


class OrigemSerializer(serializers.Serializer):
    origem = serializers.ChoiceField(choices=Origem.choices)
