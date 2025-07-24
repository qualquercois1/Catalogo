from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('meus-filmes/', views.listar_meus_filmes, name='listar_meus_filmes'),

    path('register/', views.register_view, name='register'),

    path('item/novo/', views.criar_item_view, name='criar_item'),

    path('item/<int:item_id>/', views.detalhe_item_view, name='detalhe_item'),
]