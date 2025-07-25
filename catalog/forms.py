# catalog/forms.py

from django import forms # Importe 'forms' diretamente
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, Ator, Diretor

class CustomUserCreationForm(forms.ModelForm):
    # 1. Definimos os campos de senha manualmente, pois eles não existem no modelo User.
    #    Usamos o widget PasswordInput para que o texto fique escondido (•••••).
    password_1 = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput
    )
    password_2 = forms.CharField(
        label='Confirmação de Senha', 
        widget=forms.PasswordInput,
        help_text="Digite a mesma senha para confirmar."
    )

    class Meta:
        model = User
        # 2. Definimos os campos que virão do modelo User.
        fields = ('username', 'email')
        labels = {
            'username': 'Nome de Usuário',
            'email': 'E-mail (obrigatório)',
        }
        help_texts = {
            'email': 'Obrigatório. Um e-mail válido para contato.',
        }

    # 3. Usamos o método clean() para a validação geral do formulário.
    def clean(self):
        # Primeiro, rodamos a validação padrão do ModelForm.
        super().clean()
        
        # Agora, pegamos os valores dos campos de senha do dicionário cleaned_data.
        password_1 = self.cleaned_data.get("password_1")
        password_2 = self.cleaned_data.get("password_2")

        # Verificamos se as duas senhas foram digitadas e se são diferentes.
        if password_1 and password_2 and password_1 != password_2:
            # Se forem diferentes, geramos um erro para o campo 'password_2'.
            self.add_error('password_2', "As duas senhas não são iguais.")

    # 4. Sobrescrevemos o método save() para lidar com a senha.
    def save(self, commit=True):
        # Pegamos a instância do usuário, mas não a salvamos ainda (commit=False).
        user = super().save(commit=False)
        
        # Pegamos a senha limpa e a definimos usando set_password().
        # Este método cuida de toda a criptografia (hashing) necessária.
        user.set_password(self.cleaned_data["password_1"])
        
        # Se commit for True, salvamos o usuário no banco de dados.
        if commit:
            user.save()
            
        return user


# A sua classe ItemForm continua igual
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['nome', 'sinopse', 'ano_lancamento', 'duracao', 'diretor', 'atores', 'generos']
        widgets = {
            'generos': forms.CheckboxSelectMultiple,
        }

class DiretorForm(forms.ModelForm):
    class Meta:
        model = Diretor
        fields = ['nome']

class AtorForm(forms.ModelForm):
    class Meta:
        model = Ator
        fields = ['nome']