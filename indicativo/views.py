from django.shortcuts import render
from .models import *
from .forms import *
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    """Retorna o template da página inicial"""
    
    return render(request, 'indicativo/index.html')

@login_required
def listar_indicativos(request):
    """A querry faz um select no banco"""
    
    indicativo = Indicativos.objects.filter(owner=request.user).order_by('data')
    context = {"indicativo": indicativo}
    
    return render(request, 'indicativo/listar.html', context)

@login_required
def buscar_indicativos(request):
    """Retorna o indicativo desejado"""    
   
    indicativo = None  # Se eu não declarar essa variável no escopo global, ela não será executada no bloco else, pois estará em um escopo local.
                       # Se a condição else não for satisfeita, a evocação da variável não ocorrerá. 
    if request.method != 'POST':  #  A primeira requisição é sempre GET.
        form = indicativosForm()
    else:
        form = indicativosForm(request.POST)  #  Pega a fita do front
       
        if form.is_valid(): 
            indicativos_queryset = Indicativos.objects.filter(nome__icontains=form.cleaned_data['nome'])  # essa query tá funcionando de boas            
            
            if not indicativos_queryset:  # Essa variável é um queryset ou seja é uma coleção de selects, é sujo e não se pode extrair dados direito como o .id
               context = {"indicativo": indicativos_queryset, "form": form}  
               return render(request, 'indicativo/resultado_busca.html', context)  
            else:
                 indicativo = indicativos_queryset.first()  # agora a variável indicativo está limpa, o primeiro elemento que der match será armazenado.              
                 context = {"indicativo": indicativo, "form": form}                    
                 return HttpResponseRedirect(reverse('indicativo:listar_radioamador', args=[indicativo.id]))  # Isso aqui envia uma lista com o id para a func listar_rdio..   
                 # No Django, o nome 'args' é uma convesão para indicar que um parâmetro passado é uma lista de argumentos posicionais, se mudar não funfa. No python pode mudar.                                                        
   
    context = {"indicativo": indicativo, "form": form}    #  Revise essa função
    return render(request, 'indicativo/buscar_indicativo.html', context)

    

@login_required
def listar_radioamador(request, id_radioamador):
    """Retorna os dados do radioamador relacionados ao indicativo selecionado"""
    
    indicativo = Indicativos.objects.get(id=id_radioamador)
    dados = indicativo.radioamador_set.order_by('-date_added')
    context = {'indicativo': indicativo, 'dados': dados}
    
    return render(request, 'indicativo/entradas.html', context)


@login_required
def adicionar_indicativo(request):
    """Insere os dados no banco de dados"""
    
    if request.method != 'POST':
        form = indicativosForm()  #  Cria uma instância vazia da representação form do model    
    else:
        form = indicativosForm(request.POST)  #  Recebe o conteúdo do front
        if form.is_valid():
            new_user = form.save(commit=False)  #  Temos que estabelecer a relação entre o usuário e o indicativo antes de salvar no db. 
            new_user.owner = request.user  # Cada indicativo deve ter um usuário atribuído.
            new_user.save()
            return HttpResponseRedirect(reverse('indicativo:listar_indicativos'))  # Redireciona para a página de indicativos Isso aqui envia um novo request, get. lembre que
            #  Uma requisição nunca deve terminar com post. A ordem para evitar erros é Get - Post - Get.
    context = {'form': form}        
    return render(request, 'indicativo/cadastrar_indicativo.html', context)


@login_required
def adicionar_entrada(request,id_radioamador):
    """Recebe os dados do radioamador"""
    
    indicativo = Indicativos.objects.get(id=id_radioamador)
    
    if indicativo.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        form = RadioAmadorForms()
    else:
        form = RadioAmadorForms(request.POST)
        if form.is_valid():
            nova_entrada = form.save(commit=False) # Armazena o conteúdo do front mas não salva no DB, pois precisamos relacionar ao indicativo.
            nova_entrada.indicativo = indicativo  # nova_entrada é uma instância de form(), herda todos seus atributos, como indicativo, ele recebe o id_radioamador feito no select
            nova_entrada.save()
            return HttpResponseRedirect(reverse('indicativo:listar_radioamador', args=[id_radioamador]))  #  The Django URL pattern require a parâmeter named 'args'
    context = {'indicativo': indicativo, 'form': form}
    return render(request, 'indicativo/cadastrar_dados.html', context) 
 

@login_required
def editar_dados(request, id_radioamador):
    """Permite editar as informações do radioamador"""
    
    dados = RadioAmador.objects.get(id=id_radioamador)
    indicativo = dados.indicativo  # Lembre-se que dados é uma instância da clase radio e herda todos os seus atributos e métodos como o indicativo   
    
    if indicativo.owner != request.user:
        raise Http404
     
    if request.method != 'POST':
        form = RadioAmadorForms(instance=dados)  # carrega o form com o conteúdo de dados e permite sua edição através do atributo instance.
    else:
        form = RadioAmadorForms(instance=dados, data=request.POST)  # dados chegam do front para serem salvos no db.  
        if form.is_valid():
            form.save(commit=False)
            return HttpResponseRedirect(reverse('indicativo:listar_radioamador', args=[indicativo.id]))  # esse arg é uma lista com os indicativos para serem manipulados no redirect
    context = {'dados': dados, 'indicativo': indicativo, 'form': form}                                   #  Sem o args, o redirect não sabe para qual página retornar.
    return render(request, 'indicativo/editar_entrada.html', context)


@login_required
def iniciar_qso(request):   # Essa entidade não está relacionada as outras, portanto não é possível estabelecer uma comparação com o objeto request.user
    """Inicia uma conversa com o radioamador"""
    
    if request.method != 'POST':
       form = ConversaForms()
    else:
        form = ConversaForms(request.POST)
        if form.is_valid(): 
           new_user = form.save()                     
           return HttpResponseRedirect(reverse('indicativo:listar_indicativos'))
    context = {'form': form}
    return render(request, 'indicativo/iniciar_qso.html', context)    


#  @login_required
def listar_qso(request):
    """Lista o histórido de conversas entre os radioamadores"""
    
    dados = Conversa.objects.order_by('-date_added')   
    context = {'dados': dados}
    return render(request, 'indicativo/listar_qso.html', context)
        
                       
    
    
    