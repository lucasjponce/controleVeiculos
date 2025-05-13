from django.urls import path, include
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login'), name='root'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro-veiculo/', views.cadastro_veiculo_view, name='cadastro_veiculo'),
    path('registro/', views.registro_view, name='registro'),
    path('historico/', views.historico_view, name='historico'),
    path('configuracoes/', views.configuracoes_view, name='configuracoes'),
    path('cadastro-usuario/', views.cadastro_usuario_view, name='cadastro_usuario'),
    path('menu/', views.menu_view, name='menu'),
]
