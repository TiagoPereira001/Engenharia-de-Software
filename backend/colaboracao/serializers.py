from rest_framework import serializers

from .models import Comentario, Notificacao, Preferencias


class ComentarioSerializer(serializers.ModelSerializer):
    autor = serializers.CharField(source="autor.username", read_only=True)
    meu = serializers.SerializerMethodField()

    class Meta:
        model = Comentario
        fields = ["id", "autor", "texto", "criado_em", "editado_em", "meu"]
        read_only_fields = ["criado_em", "editado_em"]

    def get_meu(self, comentario):
        utilizador = self.context["request"].user
        return utilizador.is_authenticated and comentario.autor_id == utilizador.pk


class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = ["id", "pedido", "tipo", "texto", "criada_em", "lida"]


class PreferenciasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preferencias
        fields = ["estados", "mencoes", "comentarios", "email"]


class LidasSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), required=False, default=list)
