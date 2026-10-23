from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Utilizador


@admin.register(Utilizador)
class UtilizadorAdmin(UserAdmin):
    list_display = ["username", "email", "papel", "is_staff"]
    list_filter = ["papel", "is_staff"]
    fieldsets = UserAdmin.fieldsets + (("Papel no projeto", {"fields": ["papel"]}),)
