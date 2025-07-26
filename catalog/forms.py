from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, Ator, Diretor

class CustomUserCreationForm(forms.ModelForm):
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
        fields = ('username', 'email')
        labels = {
            'username': 'Nome de Usuário',
            'email': 'E-mail (obrigatório)',
        }
        help_texts = {
            'email': 'Obrigatório. Um e-mail válido para contato.',
        }

    def clean(self):
        super().clean()
        
        password_1 = self.cleaned_data.get("password_1")
        password_2 = self.cleaned_data.get("password_2")

        if password_1 and password_2 and password_1 != password_2:
            self.add_error('password_2', "As duas senhas não são iguais.")

    def save(self, commit=True):
        user = super().save(commit=False)
        
        user.set_password(self.cleaned_data["password_1"])

        if commit:
            user.save()
            
        return user


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