from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate as toba
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm


def logout_view(request):
    """Desloga o usuário"""
    
    logout(request)
    return HttpResponseRedirect(reverse('indicativo:index'))  #  Lembre-se que a requisição tem que terminar com get. GET-POST-GET. O return chama a url que chama a view.


def register(request):
    """Realiza o registro de usuários"""
    
    if request.method != 'POST':
        #  Gera um formulário em branco        
        form = UserCreationForm()
    else:
        # Processa o formulário vindo do front
        form = UserCreationForm(data=request.POST)
        
        if form.is_valid():
           #  Autentica o usuário e o redireciona para a página principal     
           novo_usuario = form.save()  # Um objeto deve receber os dados do front para ser manipulado, assim mantemos o dado original e uma cópia para manipular.
           usuario_autenticado = toba(username=novo_usuario.username, password=request.POST['password1'])
           login(request, usuario_autenticado)  # cria a sessão de usuário
           return HttpResponseRedirect(reverse('indicativo:index')) # Para indicar uma função devemos mostrar a app + ':' nome da função    
    
    context = {'form': form}
    return render(request, 'users/register.html', context)
