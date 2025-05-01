from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


#class Usuario(models.Model):
#    cpf = models.CharField(max_length=14, primary_key=True)  # Ex: 000.000.000-00
#    senha = models.CharField(max_length=128)
#    papel = models.CharField(max_length=50)  # Ex: Administrador, Operador
#    funcao = models.CharField(max_length=100)

#    def __str__(self):
#        return self.cpf

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

class Veiculo(models.Model):
    id = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=10, unique=True)
    proprietario = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    # campo origem removido

    def __str__(self):
        return f"{self.placa} - {self.proprietario}"
    
class Registro(models.Model):
    id = models.AutoField(primary_key=True)
    data_hora = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=10)  # Ex: Entrada, Saída
    observacoes = models.TextField(blank=True, null=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo} - {self.veiculo.placa} em {self.data_hora}"

class ModeloVeiculo(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.marca} - {self.modelo}"

