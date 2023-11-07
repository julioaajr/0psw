from django.shortcuts import render, redirect
from django.http import request, HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout

# Create your views here.


def Cadastro(request):
    if request.method == 'GET':
        return render(request,'cadastro.html')
    elif request.method == 'POST':
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if senha != confirmar_senha :
            messages.add_message(request, constants.ERROR, 'As senhas não são iguais!')
            return redirect('cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha é menor que 6 digitos')
            return redirect('cadastro')
        user = User()
        try:
            user = User.objects.get(username= username)
        except:
            pass

        if user.id != None:
            messages.add_message(request, constants.ERROR, 'USERNAME já existe')
            return redirect('cadastro')



        try: 
            user = User.objects.create_user(
                first_name =primeiro_nome,
                last_name = ultimo_nome,
                username = username,
                email = email,
                password = senha)
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso.')
            return redirect('cadastro')
        except:
            messages.add_message(request, constants.ERROR, 'Erro não mapeado informe o SUPORTE')
            return redirect('cadastro')
        return HttpResponse('aqui')


def Login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            messages.add_message(request, constants.SUCCESS, f'Usuario {request.user.username} já esta logado')
        return render(request, "login.html")

    if request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        user = authenticate(username = username, password = senha)

        if user:
            login(request,user)
            return redirect('solicitar_exames')
        else:
            messages.add_message(request, constants.ERROR, 'Login ou senha invalidos')
            return redirect ('login')
        return HttpResponse (f"{username} -- {senha}")


def Logout(request):
    print('usuario deslogado')
    logout(request)
    return redirect('login')