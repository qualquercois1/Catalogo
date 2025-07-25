from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Genero(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

class Ator(models.Model):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome

class Diretor(models.Model):
    nome = models.CharField(max_length=60)

    def __str__(self):
        return self.nome


class Item(models.Model):
    nome = models.CharField(max_length=60)
    sinopse = models.TextField(null=True, blank=True)
    ano_lancamento = models.PositiveIntegerField()
    duracao = models.PositiveIntegerField(help_text="Duração em minutos")
    assistido = models.BooleanField(default=False)
    comentario = models.TextField(null=True, blank=True, help_text="Comentários pessoais sobre o item")
    proprietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="itens_cadastrados")
    
    diretor = models.ForeignKey(Diretor, on_delete=models.PROTECT, related_name="filmes_dirigidos")
    
    atores = models.ManyToManyField(Ator, related_name="atuou_em")
    
    generos = models.ManyToManyField(Genero, related_name="filmes_do_genero")

    def __str__(self):
        return f"{self.nome} ({self.ano_lancamento}) ({self.proprietario.username})"


class Avaliacao(models.Model):
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="avaliacoes")
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="avaliacoes")
    
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)] 
    )
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nota {self.nota} para '{self.item.nome}' por {self.usuario.username}"

    class Meta:
        unique_together = ('usuario', 'item')