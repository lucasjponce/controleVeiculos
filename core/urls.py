from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('cadastro-veiculo/', views.cadastro_veiculo_view, name='cadastro_veiculo'),
    path('registro/', views.registro_view, name='registro'),
    path('historico/', views.historico_view, name='historico'),
    path('configuracoes/', views.configuracoes_view, name='configuracoes'),
]
