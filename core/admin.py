from django.contrib import admin
from .models import Usuario, Veiculo, Registro

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

@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'data_hora', 'veiculo', 'usuario')
    search_fields = ('veiculo__placa', 'usuario__cpf')
    list_filter = ('tipo', 'data_hora')
    ordering = ('-data_hora',)