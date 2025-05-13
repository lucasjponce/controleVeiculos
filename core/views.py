from rest_framework import viewsets
from .models import Usuario, Veiculo, Registro
from .serializers import UsuarioSerializer, VeiculoSerializer, RegistroSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import VeiculoForm, RegistroForm, UsuarioCadastroForm
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.utils.dateparse import parse_date
from datetime import datetime

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
        # Autenticação usando o sistema de autenticação do Django
        # O parâmetro 'username' será comparado com o campo definido como USERNAME_FIELD no seu modelo de usuário.
        user = authenticate(request, username=cpf, password=senha)
        if user is not None:
            login(request, user)
            return redirect('menu') # mudar a pagina
        else:
            error = "CPF ou senha inválidos."
            return render(request, 'core/login.html', {'error': error})
    return render(request, 'core/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('login')

def menu_view(request):
    if request.method == "POST":
        return redirect('registro')


def cadastro_veiculo_view(request):
    if request.method == "POST":
        form = VeiculoForm(request.POST)
        if form.is_valid():
            modelo_predefinido = form.cleaned_data['modelo_predefinido']
            veiculo = form.save(commit=False)
            # preencher marca e modelo a partir do modelo_predefinido
            veiculo.marca = modelo_predefinido.marca
            veiculo.modelo = modelo_predefinido.modelo
            veiculo.save()
            return redirect('menu')
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
            return redirect('historico')
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})

def historico_view(request):
    registros = Registro.objects.select_related('veiculo', 'usuario').all()

    data = request.GET.get('data')
    tipo = request.GET.get('tipo')
    veiculo = request.GET.get('veiculo')
    proprietario = request.GET.get('proprietario')

    if data:
        try:
            data_obj = datetime.strptime(data, "%Y-%m-%d").date()
            registros = registros.filter(data_hora__date=data_obj)
        except ValueError:
            pass

    if tipo:
        registros = registros.filter(tipo=tipo)
    if veiculo:
        registros = registros.filter(veiculo__placa__icontains=veiculo)
    proprietario = request.GET.get('usuario')
    if proprietario:
        registros = registros.filter(veiculo__proprietario__icontains=proprietario)

    registros = registros.order_by('-data_hora')
    return render(request, 'core/historico.html', {'registros': registros})

def configuracoes_view(request):
    return render(request, 'core/configuracoes.html')

def menu_view(request):
    return render(request, 'core/menu.html')

def cadastro_usuario_view(request):
    if request.method == "POST":
        form = UsuarioCadastroForm(request.POST)
        if form.is_valid():
            # Salve o usuário. Você pode querer aplicar hash na senha, se necessário.
            usuario = form.save(commit=False)
            # utilizando set_password, o modelo herda de AbstractBaseUser
            usuario.set_password(form.cleaned_data['password'])
            #utilizando o make_password para hashear a senha
            #usuario.password = make_password(form.cleaned_data['senha'])
            usuario.save()
            return redirect('login')  # Redireciona para a página de login após o cadastro
    else:
        form = UsuarioCadastroForm()
    return render(request, 'core/cadastro_usuario.html', {'form': form})