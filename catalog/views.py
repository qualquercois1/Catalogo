# catalog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login # <-- A LINHA QUE FALTAVA
from django.db.models import Subquery, OuterRef
from .models import Item, Avaliacao
from .forms import CustomUserCreationForm, ItemForm


@login_required 
def listar_meus_filmes(request):
    # 1. Vamos criar uma subconsulta.
    # Para cada Item na consulta principal (OuterRef('pk')), esta subconsulta vai buscar
    # a 'nota' da Avaliacao que pertence ao usuário logado (request.user).
    minha_nota_subquery = Avaliacao.objects.filter(
        item_id=OuterRef('pk'),
        usuario=request.user
    ).values('nota')[:1] # O [:1] garante que pegamos apenas uma nota, caso haja alguma inconsistência.

    # 2. Agora, fazemos a consulta principal.
    # Buscamos todos os itens do proprietário e usamos .annotate() para adicionar um novo
    # "campo virtual" chamado 'minha_nota' a cada item, preenchido com o resultado da subconsulta.
    filmes_do_usuario = Item.objects.filter(
        proprietario=request.user
    ).annotate(
        minha_nota=Subquery(minha_nota_subquery)
    ).order_by('-id')
    
    context = {
        'filmes': filmes_do_usuario
    }
    return render(request, 'catalog/meus_filmes.html', context)

def home_view(request):
    # Vamos fazer algo simples: contar quantos filmes/séries estão cadastrados no total.
    total_itens_no_catalogo = Item.objects.count()

    # O 'contexto' é um dicionário que envia variáveis do Python para o template HTML.
    context = {
        'total_itens': total_itens_no_catalogo,
    }

    # Renderiza o arquivo HTML 'home.html' e passa o contexto para ele.
    return render(request, 'catalog/home.html', context)

def register_view(request):
    # Se o usuário já estiver logado, redireciona para a home
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # Se o formulário foi enviado (método POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # Salva o novo usuário no banco de dados
            login(request, user) # Loga o usuário automaticamente após o registro
            return redirect('home') # Redireciona para a página inicial
    else:
        # Se for o primeiro acesso à página (método GET), mostra um formulário em branco
        form = CustomUserCreationForm()
    
    return render(request, 'catalog/register.html', {'form': form})


@login_required
def criar_item_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            # Use commit=False para criar o objeto na memória sem salvar no banco ainda.
            novo_item = form.save(commit=False)
            # Associe o usuário logado como o proprietário.
            novo_item.proprietario = request.user
            # Agora sim, salve o objeto completo no banco.
            novo_item.save()
            # O save_m2m é necessário para salvar as relações ManyToMany (atores, generos)
            form.save_m2m()
            
            return redirect('catalog:detalhe_item', item_id=novo_item.id)
    else:
        form = ItemForm()
    
    return render(request, 'catalog/criar_item.html', {'form': form})

@login_required
def detalhe_item_view(request, item_id):
    # Pega o item do banco de dados pelo ID, ou retorna um erro 404 se não encontrar
    item = get_object_or_404(Item, id=item_id, proprietario=request.user)
    
    # Verifica se o usuário atual já tem uma avaliação para este item
    avaliacao_existente = Avaliacao.objects.filter(usuario=request.user, item=item).first()

    if request.method == 'POST':
        # Pega a nota enviada pelo formulário no template
        nota = request.POST.get('nota')
        if nota:
            # Cria uma nova avaliação ou atualiza a existente para este usuário e item.
            # 'defaults' garante que a nota será atualizada se a avaliação já existir.
            Avaliacao.objects.update_or_create(
                usuario=request.user,
                item=item,
                defaults={'nota': nota}
            )
        # Redireciona para a mesma página para mostrar a nota atualizada
        return redirect('catalog:detalhe_item', item_id=item.id)

    context = {
        'item': item,
        'avaliacao_existente': avaliacao_existente,
        'range_notas': range(1, 11) # Gera uma sequência de 1 a 10 para o formulário
    }
    return render(request, 'catalog/detalhe_item.html', context)