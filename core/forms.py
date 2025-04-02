from django import forms
from .models import Veiculo, Registro

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa', 'marca', 'modelo', 'origem']
        widgets = {
            'placa': forms.TextInput(attrs={'placeholder': 'Placa'}),
            'marca': forms.TextInput(attrs={'placeholder': 'Marca'}),
            'modelo': forms.TextInput(attrs={'placeholder': 'Modelo'}),
            'origem': forms.TextInput(attrs={'placeholder': 'Origem'}),
        }

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['tipo', 'observacoes', 'veiculo']
        widgets = {
            'tipo': forms.Select(choices=[('Entrada', 'Entrada'), ('Saída', 'Saída')]),
            'observacoes': forms.Textarea(attrs={'placeholder': 'Observações'}),
        }