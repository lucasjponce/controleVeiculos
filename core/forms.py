from django import forms
from .models import Veiculo, Registro, Usuario

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
        
class UsuarioCadastroForm(forms.ModelForm):
    senha2 = forms.CharField(widget=forms.PasswordInput, label="Confirme a Senha")
    
    class Meta:
        model = Usuario
        fields = ['cpf', 'senha', 'papel', 'funcao']
        widgets = {
            'senha': forms.PasswordInput,
        }
        labels = {
            'cpf': 'CPF',
            'senha': 'Senha',
            'papel': 'Papel',
            'funcao': 'Função',
        }

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senha2 = cleaned_data.get("senha2")
        if senha and senha2 and senha != senha2:
            self.add_error('senha2', "As senhas não conferem!")
        return cleaned_data
