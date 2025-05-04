from django.contrib import admin
from .models import Usuario, Veiculo

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'papel', 'funcao', 'is_staff')
    search_fields = ('cpf', 'funcao')
    list_filter = ('papel', 'is_staff')
    ordering = ('cpf',)

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'proprietario', 'marca', 'modelo')
    search_fields = ('placa', 'proprietario')
    list_filter = ('marca',)
    ordering = ('placa',)
