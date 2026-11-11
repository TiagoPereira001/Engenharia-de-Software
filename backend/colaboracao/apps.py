from django.apps import AppConfig


class ColaboracaoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "colaboracao"
    verbose_name = "Colaboração"

    def ready(self):
        # Liga os avisos às mudanças de estado dos pedidos (ver sinais.py).
        from . import sinais  # noqa: F401
