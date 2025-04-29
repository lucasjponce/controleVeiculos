from django import forms
from .models import Veiculo, Registro, Usuario, ModeloVeiculo
from collections import defaultdict

def validar_cpf(cpf: str) -> bool:
        cpf = ''.join(filter(str.isdigit, cpf))  # Remove qualquer coisa que não for número
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        for i in range(9, 11):
            soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
            digito = ((soma * 10) % 11) % 10
            if int(cpf[i]) != digito:
                return False
        return True

class VeiculoForm(forms.ModelForm):
    modelo_predefinido = forms.ModelChoiceField(
        queryset=ModeloVeiculo.objects.all().order_by('marca', 'modelo'),
        required=False,
        label="Escolha Marca e Modelo",
        empty_label="--- Selecione ---"
    )

    class Meta:
        model = Veiculo
        fields = ['placa', 'marca', 'modelo', 'origem']
        widgets = {
            'placa': forms.TextInput(attrs={'placeholder': 'Placa'}),
            'marca': forms.TextInput(attrs={'placeholder': 'Marca'}),
            'modelo': forms.TextInput(attrs={'placeholder': 'Modelo'}),
            'origem': forms.TextInput(attrs={'placeholder': 'Origem'}),
        }

    def __init__(self, *args, **kwargs):
        super(VeiculoForm, self).__init__(*args, **kwargs)
        self.fields['marca'].widget.attrs['readonly'] = True
        self.fields['modelo'].widget.attrs['readonly'] = True
        # Agrupar veículos por marca
        veiculos = Veiculo.objects.all().order_by('marca', 'modelo')
        marcas = defaultdict(list)
        for v in veiculos:
            marcas[v.marca].append((f"{v.marca}-{v.modelo}", v.modelo))

        # Monta a lista de opções agrupadas
        choices = [('', '--- Selecione um veículo ---')]
        for marca, modelos in marcas.items():
            for value, modelo in modelos:
                choices.append((value, f"{marca} - {modelo}"))
        self.fields['modelo_predefinido'].choices = choices    

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
        fields = ['cpf', 'password', 'papel', 'funcao']
        widgets = {
            'password': forms.PasswordInput,
        }
        labels = {
            'cpf': 'CPF',
            'password': 'Password',
            'papel': 'Papel',
            'funcao': 'Função',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        senha= cleaned_data.get("password")
        senha2 = cleaned_data.get("senha2")

        if senha and senha2 and senha != senha2:
            self.add_error('senha2', "As senhas não conferem!")
        
        cpf = cleaned_data.get('cpf')
        if cpf and not validar_cpf(cpf):
            self.add_error('cpf', "CPF inválido!")
        
        return cleaned_data
