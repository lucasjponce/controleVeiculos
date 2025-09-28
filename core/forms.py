from django import forms
from .models import Veiculo, Registro, Usuario, ModeloVeiculo

PAPEIS_CHOICES = [
    ('usuario', 'Usuário'),
    ('administrador', 'Administrador')
]

def validar_cpf(cpf: str) -> bool:
    cpf = ''.join(filter(str.isdigit, cpf))
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
        required=True,
        label="Escolha Marca e Modelo",
        empty_label="--- Selecione ---"
    )

    class Meta:
        model = Veiculo
        fields = ['placa', 'proprietario']
        widgets = {
            'placa': forms.TextInput(attrs={
                'placeholder': 'AAA1234',
                'style': 'text-transform:uppercase;',
                'maxlength': '8'
            }),
            'proprietario': forms.TextInput(attrs={'placeholder': 'Proprietário'}),
        }
        labels ={
            'placa': 'Placa do Veiculo',
            'proprietario': 'Nome do Proprietario'
        }

    def __init__(self, *args, **kwargs):
        super(VeiculoForm, self).__init__(*args, **kwargs)

    def clean_placa(self):
        placa = self.cleaned_data['placa'].upper().replace("-", "")

        # Verifica se tem exatamente 7 caracteres
        if len(placa) != 7:
            raise forms.ValidationError("A placa deve conter exatamente 7 caracteres.")

        # Valida padrão: 3 letras + 4 números/letras
        import re
        if not re.match(r'^[A-Z]{3}[0-9A-Z]{4}$', placa):
            raise forms.ValidationError("Formato de placa inválido. Use o formato AAA1234.")

        return placa    

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
    papel = forms.ChoiceField(choices=PAPEIS_CHOICES, required=True)

    class Meta:
        model = Usuario
        fields = ['cpf', 'password', 'papel']
        widgets = {
            'password': forms.PasswordInput,
        }
        labels = {
            'cpf': 'CPF',
            'password': 'Senha',
            'papel': 'Papel',
        }

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("password")
        senha2 = cleaned_data.get("senha2")

        if senha and senha2 and senha != senha2:
            self.add_error('senha2', "As senhas não conferem!")

        cpf = cleaned_data.get('cpf')
        if cpf and not validar_cpf(cpf):
            self.add_error('cpf', "CPF inválido!")

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # senha criptografada

        # se papel for administrador = superusuario Django
        if self.cleaned_data.get("papel") == "administrador":
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False

        if commit:
            user.save()
        return user
