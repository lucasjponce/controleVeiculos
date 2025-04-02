from rest_framework import viewsets
from .models import Usuario, Veiculo, Registro
from .serializers import UsuarioSerializer, VeiculoSerializer, RegistroSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import VeiculoForm, RegistroForm

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer

class RegistroViewSet(viewsets.ModelViewSet):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer

def login_view(request):
    if request.method == "POST":
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')
        # Aqui você pode fazer a autenticação, por exemplo, usando o sistema de autenticação do Django
        user = authenticate(request, username=cpf, password=senha)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "CPF ou senha inválidos."
            return render(request, 'core/login.html', {'error': error})
    return render(request, 'core/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    total_veiculos = Veiculo.objects.count()
    entradas_hoje = Registro.objects.filter(tipo='Entrada').count()  # ajuste para filtrar pela data
    saidas_hoje = Registro.objects.filter(tipo='Saída').count()      # ajuste para filtrar pela data
    context = {
        'total_veiculos': total_veiculos,
        'entradas_hoje': entradas_hoje,
        'saidas_hoje': saidas_hoje,
    }
    return render(request, 'core/dashboard.html', context)

def cadastro_veiculo_view(request):
    if request.method == "POST":
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = VeiculoForm()
    return render(request, 'core/cadastro_veiculo.html', {'form': form})

def registro_view(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            # Se desejar associar o usuário logado:
            registro.usuario = request.user  
            registro.save()
            return redirect('dashboard')
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})

def historico_view(request):
    registros = Registro.objects.all().order_by('-data_hora')
    return render(request, 'core/historico.html', {'registros': registros})

def configuracoes_view(request):
    return render(request, 'core/configuracoes.html')