from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item
from django import forms

# Vamos usar o formulário padrão do Django para criar usuários.
# Se no futuro você quisesse adicionar campos extras (ex: data de nascimento),
# você customizaria este formulário. Por enquanto, o padrão é perfeito.
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # Você pode definir os campos que quer no formulário aqui, se necessário
        # fields = ('username', 'email')
        pass # Usando 'pass' para herdar todos os comportamentos padrão.

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        # Defina os campos do modelo 'Item' que o usuário poderá preencher.
        # Excluímos campos que não fazem sentido para o usuário preencher no cadastro inicial.
        fields = ['nome', 'sinopse', 'ano_lancamento', 'duracao', 'diretor', 'atores', 'generos']