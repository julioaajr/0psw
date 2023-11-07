from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
from django.utils import timezone

# Create your views here.
# Aula 3
@login_required
def Solicitar_exames(request):
    tipos_exames = TipoExames.objects.all()
    if request.method == 'GET':
        
        return render(request,'solicitar_exames.html',{'tipos_exames':tipos_exames})
    

    elif request.method == 'POST':
        exames_id = request.POST.getlist('exames')
        solicitacao_exames = TipoExames.objects.filter(id__in = exames_id)
        preco_total =0
        for i in solicitacao_exames:
            if i.disponivel:
                preco_total += i.preco
        print(solicitacao_exames)
        return render(request,'solicitar_exames.html',{'tipos_exames':tipos_exames,
                                                       'solicitacao_exames':solicitacao_exames,
                                                       'preco_total': preco_total })
    
@login_required
def Fechar_pedido(request):
    exames_id = request.POST.getlist('exames')
    if exames_id != []:
        solicitacao_exames = TipoExames.objects.filter(id__in =exames_id)

        pedido_exame = PedidosExames(
            usuario = request.user,
            data = datetime.now()
        )
        pedido_exame.save()

        for exame in solicitacao_exames:
            solicitacao_exames_temp = SolicitacaoExame(
                usuario = request.user,
                exame = exame,
                status = "E"
            )
            solicitacao_exames_temp.save()
            pedido_exame.exames.add(solicitacao_exames_temp)

        pedido_exame.save()
        messages.add_message(request, constants.SUCCESS, 'Pedido SALVO COM SUCESSO')
    else:
        messages.add_message(request, constants.ERROR, 'Pedido Vazio')
    return redirect('gerenciar_pedidos')


@login_required
def Gerenciar_pedidos(request):
    pedidos_exames = PedidosExames.objects.filter(usuario = request.user)
    return render(request, 'gerenciar_pedidos.html', {'pedidos_exames':pedidos_exames})


@login_required
def Cancelar_pedido(request, pedido_id):
    pedido_exames = PedidosExames.objects.get(id = pedido_id)
    if pedido_exames.usuario == request.user:
        pedido_exames.agendado = False
        pedido_exames.save()
        messages.add_message(request,constants.SUCCESS,'Pedido Cancelado')
        return redirect('gerenciar_pedidos')
    messages.add_message(request,constants.ERROR,'Erro o pedido não lhe pertence')
    return redirect('gerenciar_pedidos')

@login_required
def Gerenciar_exames(request):
    pedido =  PedidosExames.objects.filter(usuario = request.user, agendado = True)
    exames = SolicitacaoExame.objects.filter(pedidosexames__in=pedido)
    #print(x)
    #exames = SolicitacaoExame.objects.filter(usuario=request.user)
    return render(request, 'gerenciar_exames.html', {'exames': exames})


@login_required
def Permitir_abrir_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id = exame_id, usuario = request.user)
    if not exame.requer_senha:
        if exame.resultado:
            return redirect(exame.resultado.url)
        else:
            return HttpResponse ('Sem laudo para esse exame')        
    else:
        if exame.resultado:
            return redirect('solicitar_senha_exame' ,exame_id = exame_id)
        else:
            return HttpResponse ('Sem laudo para esse exame')      
    
    return redirect ('Sem laudo incluso')


@login_required
def Solicitar_senha_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id = exame_id, usuario = request.user)
    if request.method == 'GET':
        return render(request,'solicitar_senha_exame.html',{'exame':exame})
    elif request.method == 'POST':
        senha = request.POST.get('senha')
        if senha == exame.senha:
            if exame.resultado:
                return redirect(exame.resultado.url)
            else:
                return HttpResponse ('Sem laudo para esse exame')      
        else:
            messages.add_message(request,constants.ERROR,'Senha Incorreta')
            return redirect('solicitar_senha_exame' ,exame_id = exame_id)    


def Gerar_acesso_medico (request):
    if request.method == 'GET':
        acessos_medicos = AcessoMedico.objects.filter(usuario = request.user)
        return render(request, 'gerar_acesso_medico.html', {'acessos_medicos': acessos_medicos})
    elif request.method == "POST":
        identificacao = request.POST.get('identificacao')
        tempo_de_acesso = request.POST.get('tempo_de_acesso')
        data_exame_inicial = request.POST.get("data_exame_inicial")
        data_exame_final = request.POST.get("data_exame_final")

        acesso_medico = AcessoMedico(
            usuario = request.user,
            identificacao = identificacao,
            tempo_de_acesso = tempo_de_acesso,
            data_exames_iniciais = data_exame_inicial,
            data_exames_finais = data_exame_final,
            criado_em = datetime.now()
        )

        acesso_medico.save()

        messages.add_message(request, constants.SUCCESS, 'Acesso gerado com sucesso')
        return redirect('/exames/gerar_acesso_medico')


def Acesso_medico(request,token):
    acesso_medico = AcessoMedico.objects.get(token = token)
    if acesso_medico.status == 'Expirado':
        messages.add_message(request,constants.ERROR,'Token Expirado')
        return redirect('login')

    pedidos = PedidosExames.objects.filter(usuario = acesso_medico.usuario,data__gte = acesso_medico.data_exames_iniciais,data__lte = acesso_medico.data_exames_finais)
    print(pedidos)

    return render(request,'acesso_medico.html',{'pedidos':pedidos})
    