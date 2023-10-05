from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

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
    

def Fechar_pedido(request):
    print(request.POST)
    return HttpResponse('teste')