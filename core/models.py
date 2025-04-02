from django.db import models

class Usuario(models.Model):
    cpf = models.CharField(max_length=14, primary_key=True)  # Ex: 000.000.000-00
    senha = models.CharField(max_length=128)
    papel = models.CharField(max_length=50)  # Ex: Administrador, Operador
    funcao = models.CharField(max_length=100)

    def __str__(self):
        return self.cpf

class Veiculo(models.Model):
    id = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    origem = models.CharField(max_length=50)

    def __str__(self):
        return self.placa

class Registro(models.Model):
    id = models.AutoField(primary_key=True)
    data_hora = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=10)  # Ex: Entrada, Saída
    observacoes = models.TextField(blank=True, null=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo} - {self.veiculo.placa} em {self.data_hora}"
