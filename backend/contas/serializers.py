from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Utilizador


class UtilizadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilizador
        fields = ["id", "username", "email", "papel"]
        read_only_fields = ["papel"]


class RegistoSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Utilizador
        fields = ["username", "email", "password"]

    def validate_password(self, valor):
        validate_password(valor)
        return valor

    def create(self, dados):
        # O papel fica sempre "cliente"; os outros atribui-os um administrador.
        return Utilizador.objects.create_user(**dados)
