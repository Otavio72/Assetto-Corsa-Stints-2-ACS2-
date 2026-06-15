from django.shortcuts import render, redirect
from .forms import CustomCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

#from impressa_app.models import  Pedido


# Exibe a página de perfil do usuário logado com a lista de pedidos realizados,
# ordenados do mais recente para o mais antigo

#@login_required
#def perfil(request):
 #   pedidos = Pedido.objects.filter(user=request.user).order_by('-data_criado')

  #  return render(request, 'perfil.html', {
   #     'pedidos': pedidos,
    #})

@login_required
def perfil(request):
    return render(request, 'perfil.html', {
    })
 

# Exibe a página de registro de usuário.
# Se for uma requisição POST, valida o formulário, salva o novo usuário e redireciona para o login.
def register(request):
    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
    else:
        form = CustomCreationForm()
    return render(request, 'register.html', {'form':form})


# Exibe a página de login.
# Se for uma requisição POST, autentica o usuário com os dados fornecidos.
# Se as credenciais estiverem corretas, redireciona para a página inicial.
# Caso contrário, exibe uma mensagem de erro.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha invalidos')

    return render(request, 'login.html')


# Encerra a sessão do usuário autenticado.
# Após o logout, redireciona para a página de login.
def logout_view(request):
    logout(request)
    return redirect('login')