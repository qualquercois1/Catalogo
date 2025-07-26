# catalog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login 
from django.db.models import Subquery, OuterRef
from .models import Item, Avaliacao, Diretor, Ator
from .forms import CustomUserCreationForm, ItemForm,  DiretorForm, AtorForm
from django.contrib.auth.views import LoginView, LogoutView


@login_required 
def listar_meus_filmes(request):
    minha_nota_subquery = Avaliacao.objects.filter(
        item_id=OuterRef('pk'),
        usuario=request.user
    ).values('nota')[:1] 

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
    total_itens_no_catalogo = Item.objects.count()

    context = {
        'total_itens': total_itens_no_catalogo,
    }

    return render(request, 'catalog/home.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') 
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'catalog/register.html', {'form': form})


@login_required
def criar_item_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            novo_item = form.save(commit=False)
            novo_item.proprietario = request.user
            novo_item.save()
            form.save_m2m()
            
            return redirect('catalog:detalhe_item', item_id=novo_item.id)
    else:
        form = ItemForm()
    
    return render(request, 'catalog/criar_item.html', {'form': form})

@login_required
def detalhe_item_view(request, item_id):
    item = get_object_or_404(Item, id=item_id, proprietario=request.user)
    
    avaliacao_existente = Avaliacao.objects.filter(usuario=request.user, item=item).first()

    if request.method == 'POST':
        nota = request.POST.get('nota')
        if nota:
            Avaliacao.objects.update_or_create(
                usuario=request.user,
                item=item,
                defaults={'nota': nota}
            )
        return redirect('catalog:detalhe_item', item_id=item.id)

    context = {
        'item': item,
        'avaliacao_existente': avaliacao_existente,
        'range_notas': range(1, 11) 
    }
    return render(request, 'catalog/detalhe_item.html', context)

class CustomLoginView(LoginView):
    template_name = 'catalog/login.html'
    redirect_authenticated_user = True


@login_required
def criar_diretor_popup(request):
    form = DiretorForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return render(request, "catalog/popup_close.html", {'instance_pk': instance.pk, 'instance_name': str(instance)})
    
    return render(request, "catalog/popup_form.html", {'form': form, 'title': 'Adicionar Novo Diretor'})

@login_required
def criar_ator_popup(request):
    form = AtorForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return render(request, "catalog/popup_close.html", {'instance_pk': instance.pk, 'instance_name': str(instance)})

    return render(request, "catalog/popup_form.html", {'form': form, 'title': 'Adicionar Novo Ator'})