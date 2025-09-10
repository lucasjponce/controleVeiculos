from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator

# ===== Validador de placa =====
placa_validator = RegexValidator(
    regex=r'^[A-Z]{3}[0-9A-Z]{4}$',
    message='A placa deve estar no formato AAA1234 (3 letras seguidas de 4 letras/números)'
)

# ===== Gerenciador personalizado de usuário =====
class UsuarioManager(BaseUserManager):
    def create_user(self, cpf, password=None, **extra_fields):
        if not cpf:
            raise ValueError("O CPF deve ser informado")
        user = self.model(cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(cpf, password, **extra_fields)

# ===== Modelo de Usuário =====
class Usuario(AbstractBaseUser, PermissionsMixin):
    cpf = models.CharField(max_length=14, unique=True, primary_key=True)
    password = models.CharField(max_length=128)  # Use "password" aqui
    papel = models.CharField(max_length=50)
    funcao = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['papel', 'funcao']

    def __str__(self):
        return self.cpf

# ===== Modelo de Veículo =====
class Veiculo(models.Model):
    id = models.AutoField(primary_key=True)
    placa = models.CharField(
        max_length=10,
        validators=[placa_validator],
        unique=True
    )
    proprietario = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.placa} - {self.proprietario}"
    
    def save(self, *args, **kwargs):
        if self.placa:
            self.placa = self.placa.upper().replace("-", "")
        super().save(*args, **kwargs)

# ===== Modelo de Registro de Entrada/Saída =====    
class Registro(models.Model):
    id = models.AutoField(primary_key=True)
    data_hora = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=10)  # Ex: Entrada, Saída
    observacoes = models.TextField(blank=True, null=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        Usuario, 
        to_field='cpf',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.tipo} - {self.veiculo.placa} em {self.data_hora}"

# ===== Modelo de veículos predefinidos =====
class ModeloVeiculo(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.marca} - {self.modelo}"

