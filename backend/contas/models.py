from django.contrib.auth.models import AbstractUser
from django.db import models


class Papel(models.TextChoices):
    CLIENTE = "cliente", "Cliente"
    PRODUCT_MANAGER = "product_manager", "Product manager"
    PRODUCT_OWNER = "product_owner", "Product Owner"
    PROGRAMADOR = "programador", "Programador"
    GESTOR_PROJETO = "gestor_projeto", "Gestor de projeto"


class Utilizador(AbstractUser):
    """Utilizador do sistema. Quem se regista começa como cliente (US-30)."""

    papel = models.CharField(max_length=20, choices=Papel.choices, default=Papel.CLIENTE)

    @property
    def gere_pedidos(self):
        """Product manager e Product Owner podem mudar o estado dos pedidos."""
        return self.papel in (Papel.PRODUCT_MANAGER, Papel.PRODUCT_OWNER)

    def __str__(self):
        return self.username
