from django.contrib import admin
from .models import Genero, Ator, Diretor, Item, Avaliacao

class ItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ano_lancamento', 'diretor', 'assistido')
    search_fields = ('nome', 'diretor__nome')
    list_filter = ('assistido', 'generos', 'ano_lancamento')

class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('item', 'usuario', 'nota', 'data_avaliacao')
    list_filter = ('nota', 'data_avaliacao')
    search_fields = ('item__nome', 'usuario__username')


admin.site.register(Genero)
admin.site.register(Ator)
admin.site.register(Diretor)
admin.site.register(Avaliacao, AvaliacaoAdmin)
admin.site.register(Item, ItemAdmin) 