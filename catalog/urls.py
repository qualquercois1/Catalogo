from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'catalog'

urlpatterns = [
    path('meus-filmes/', views.listar_meus_filmes, name='listar_meus_filmes'),

    path('register/', views.register_view, name='register'),

    path('item/novo/', views.criar_item_view, name='criar_item'),

    path('item/<int:item_id>/', views.detalhe_item_view, name='detalhe_item'),

    path('login/', views.CustomLoginView.as_view(), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('diretor/novo/popup/', views.criar_diretor_popup, name='criar_diretor_popup'),
    
    path('ator/novo/popup/', views.criar_ator_popup, name='criar_ator_popup'),
]