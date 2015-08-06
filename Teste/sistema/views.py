# -*- encoding: utf-8 -*-
import threading
import urllib2

from django.http.response import HttpResponse  # , HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render_to_response  # , redirect
from django.template.context import RequestContext

from sistema.formularios import FormularioLinkProjeto
from sistema.models import VerificadorProjetos, Projeto, Estado, CalcularNota,\
    ValorMedio


def index(request):
    return render_to_response("index.html")


def checar_conexao():
    import socket
    confiaveis = ['www.google.com', 'www.yahoo.com', 'www.bb.com.br']
    for host in confiaveis:
        a=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        a.settimeout(.5)
        
        try:
            b=a.connect_ex((host, 80))
            if b==0: #ok, conectado
                return True
        except:
            pass
        a.close()
    return False

def analisar_projetos(request):
    if checar_conexao():
        
        total = Projeto.objects.count()
        thread = analisar_projetos_cadastrados()
        thread.start()            
        #print "Cadastrando Projetos em Segundo Plano ."
        
        return render_to_response("analisar_projetos.html",{'num_projetos':total})
    
    return HttpResponse(u"Erro de Conexão com a Internet!")
    
def atualizar_barra_progresso_analise(request):
    
    total_projetos = Projeto.objects.count()
    
    projetos_atualizados = Projeto.objects.filter(Atualizado=1)
    
    total_projetos = float(total_projetos)
    projetos_atualizados = float(len(projetos_atualizados))
    
    print "Projetos Atualizados: ",projetos_atualizados
    print "Total Projetos:       ",total_projetos
       
    percentual = int((projetos_atualizados/total_projetos)*100)  
    
    #print "Projetos Atualizados: ",percentual
    return HttpResponse(percentual)

class analisar_projetos_cadastrados(threading.Thread):
    
    def run(self):
        contador = 0
        projetos_desatualizados = Projeto.objects.filter(Atualizado=0)
        print "Projetos Desatualizados: ",projetos_desatualizados
        for projeto in projetos_desatualizados:
            estado = VerificadorProjetos().Analisar(projeto)
            estado.save()
            estado.Nota = CalcularNota(estado)
            estado.save()
            projetos_desatualizados[contador].Atualizado = True
            projetos_desatualizados[contador].save()
            contador = contador+1
        
        #print "Forcar Desatualizacao para permitir novas Analises: "
        #projetos_atualizados = Projeto.objects.all()
        #contador = 0
        #for projeto in projetos_atualizados:
        #    projetos_atualizados[contador].Atualizado = False
        #    projetos_atualizados[contador].save()
        #    contador = contador + 1

def projeto(request,projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    estado_atual = Estado.objects.filter(Projeto_id=projeto).latest("id")
    lista_estados = Estado.objects.filter(Projeto_id=projeto)
    
    complexidade_media = ValorMedio("ComplexidadePorMetodo") 
    duplicacao_media = ValorMedio("TaxaDuplicacao")
    divida_media = ValorMedio("TaxaDividaTecnica")
    
    if estado_atual.ComplexidadePorMetodo < complexidade_media:
        cor_painel_complexidade = "primary"
        icone_painel_complexidade = "fa fa-thumbs-o-up fa-5x"
    else:
        cor_painel_complexidade = "yellow"
        icone_painel_complexidade = "fa fa-thumbs-o-down fa-5x"
        
    if estado_atual.TaxaDuplicacao < duplicacao_media:
        cor_painel_duplicacao = "primary"
        icone_painel_duplicacao = "fa fa-thumbs-o-up fa-5x"
    else:
        cor_painel_duplicacao = "yellow"
        icone_painel_duplicacao = "fa fa-thumbs-o-down fa-5x"
        
    if estado_atual.TaxaDividaTecnica < divida_media:
        cor_painel_divida = "primary"
        icone_painel_divida = "fa fa-thumbs-o-up fa-5x"
    else:
        cor_painel_divida = "yellow"
        icone_painel_divida = "fa fa-thumbs-o-down fa-5x"
    
    if estado_atual.Nota > 9.0:
        cor_painel_nota = "green"
        icone_painel_nota = "fa fa-bar-chart fa-5x"
        
    elif estado_atual.Nota > 7.0:
        cor_painel_nota = "primary"
        icone_painel_nota = "fa fa-bar-chart fa-5x"    
        
    elif estado_atual.Nota > 6.0:
        cor_painel_nota = "yellow"
        icone_painel_nota = "fa fa-bar-chart fa-5x"
    else:
        cor_painel_nota = "red"
        icone_painel_nota = "fa fa-bar-chart fa-5x"
        
    dados = {'projeto':projeto,
             'estado_atual':estado_atual,
             'lista_estados':lista_estados,
             'complexidade_media':complexidade_media,
             'duplicacao_media':duplicacao_media,
             'divida_media':divida_media,
             
             'cor_painel_complexidade':cor_painel_complexidade,
             'cor_painel_duplicacao':cor_painel_duplicacao,
             'cor_painel_divida':cor_painel_divida,
             'cor_painel_nota':cor_painel_nota,
             
             'icone_painel_complexidade':icone_painel_complexidade,
             'icone_painel_duplicacao':icone_painel_duplicacao,
             'icone_painel_divida':icone_painel_divida,
             'icone_painel_nota':icone_painel_nota
             }
    
    #total = VerificadorProjetos().getTotalNemoLinks()
    #LinksBaixados = Projeto.objects.count()
    #if LinksBaixados < total:
    #    thread = CadastrarProjetosNemo()
    #    thread.start()            
    #print "Cadastrando Projetos em Segundo Plano ."
    return render_to_response("projeto.html",dados)

def atualizar_barra_progresso(request,num_links):
    LinksCadastrados = float(Projeto.objects.count())
    num_links = float(num_links)   
    percentual = int((LinksCadastrados/num_links)*100)  
    return HttpResponse(percentual)

def cadastrar_projetos_nemo(request):
    total = VerificadorProjetos().getTotalNemoLinks()
    LinksBaixados = Projeto.objects.count()
    if LinksBaixados < total:
        thread = CadastrarProjetosNemo()
        thread.start()            
    #print "Cadastrando Projetos em Segundo Plano ."
    return render_to_response("cadastrar-projetos-nemo.html",{'num_links':total,'lista_links':None})

class CadastrarProjetosNemo(threading.Thread):
    
    def run(self):
        LinksProjetos = VerificadorProjetos().getNemoLinks()
        LinksBaixados = Projeto.objects.count()
        for url in LinksProjetos[LinksBaixados:]:
            projeto = CadastrarProjeto(url)
            try:
                projeto.save()
            except:
                pass       
        
def CadastrarProjeto(url):
    nome, linguagem = VerificadorProjetos().BuscarInformacaoBasica(url)
    projeto = Projeto()
    projeto.Nome = nome
    projeto.Link = url
    projeto.Linguagem = linguagem
    return projeto


class ParametroProjeto():
    id = None
    Nome              = None
    Linguagem         = None
    UltimaAtualizacao = None
    Complexidade      = None
    Duplicacao        = None
    DividaTecnica     = None
    Nota              = None
    
    NumeroLinhasCodigo = None
    NumeroMetodos = None
    ComplexidadeTotal = None
    
    NumeroProblemasMuitoCriticos = None
    NumeroProblemasCriticos= None
    NumeroProblemasModerados= None
    NumeroProblemasNormais= None
    NumeroProblemasSimples= None
    
    
def cadastro_projetos(request):
    lista_projetos = Projeto.objects.all()
    projetos = []
    
    for item in lista_projetos:
        estado = Estado.objects.filter(Projeto_id=item).latest("id")
        
        projeto = ParametroProjeto()
        projeto.id = item.id
        projeto.Nome = item.Nome
        projeto.Linguagem = item.Linguagem
        
        projeto.NumeroLinhasCodigo = estado.NumeroLinhasCodigo
        projeto.NumeroMetodos = estado.NumeroMetodos
        projeto.ComplexidadeTotal = int(estado.ComplexidadeTotal)
        
        projeto.UltimaAtualizacao = estado.Data
        projeto.Complexidade = estado.ComplexidadePorMetodo
        projeto.Duplicacao = estado.TaxaDuplicacao
        projeto.DividaTecnica = estado.TaxaDividaTecnica
        
        projeto.NumeroProblemasMuitoCriticos = estado.NumeroProblemasMuitoCriticos
        projeto.NumeroProblemasCriticos = estado.NumeroProblemasCriticos
        projeto.NumeroProblemasModerados = estado.NumeroProblemasModerados
        projeto.NumeroProblemasNormais = estado.NumeroProblemasNormais
        projeto.NumeroProblemasSimples = estado.NumeroProblemasSimples
        
        projeto.Nota = estado.Nota
        projetos.append(projeto)
        
    if (request.method == "POST"):
        form = FormularioLinkProjeto(request.POST, request.FILES)
        
        if form.is_valid():
            form.cleaned_data['Link']
            url = request.POST['Link']
            nome,linguagem = VerificadorProjetos().BuscarInformacaoBasica(url)
            item = Projeto()
            item.Nome = nome
            item.Link = url
            item.ProjetoUsuario = True
            item.Linguagem = linguagem
            item.save()
    else:
        form = FormularioLinkProjeto()
    
    return render_to_response("cadastro_projetos.html",{'lista_projetos':projetos,'form':form},context_instance=RequestContext(request))

def meus_projetos(request):
    lista_projetos = Projeto.objects.filter(ProjetoUsuario=True)
    projetos = []
    
    for item in lista_projetos:
        estado = Estado.objects.filter(Projeto_id=item).latest("id")
        
        projeto = ParametroProjeto()
        projeto.id = item.id
        projeto.Nome = item.Nome
        projeto.Linguagem = item.Linguagem
        projeto.UltimaAtualizacao = estado.Data
        projeto.Complexidade = estado.ComplexidadePorMetodo
        projeto.Duplicacao = estado.TaxaDuplicacao
        projeto.DividaTecnica = estado.TaxaDividaTecnica
        projeto.Nota = estado.Nota
        projetos.append(projeto)
        
    if (request.method == "POST"):
        form = FormularioLinkProjeto(request.POST, request.FILES)
        
        if form.is_valid():
            form.cleaned_data['Link']
            url = request.POST['Link']
            nome,linguagem = VerificadorProjetos().BuscarInformacaoBasica(url)
            item = Projeto()
            item.Nome = nome
            item.Link = url
            item.ProjetoUsuario = True
            item.Linguagem = linguagem
            item.save()
    else:
        form = FormularioLinkProjeto()
    
    return render_to_response("meus_projetos.html",{'lista_projetos':projetos,'form':form},context_instance=RequestContext(request))


def cadastro_fontes(request):
    lista_projetos = Projeto.objects.all()
    
    if not lista_projetos.exists():
        return redirect("/cadastrar-projetos-nemo")         
    
    if (request.method == "POST"):
        form = FormularioLinkProjeto(request.POST, request.FILES)
        
        if form.is_valid():
            form.cleaned_data['Link']
            url = request.POST['Link']
            nome,linguagem = VerificadorProjetos().BuscarInformacaoBasica(url)
            item = Projeto()
            item.Nome = nome
            item.Link = url
            item.Linguagem = linguagem
            item.save()
    else:
        form = FormularioLinkProjeto()
    
    return render_to_response("projetos.html",{'lista_projetos':lista_projetos,'form':form},context_instance=RequestContext(request))
    
def tables(request):
    return render_to_response("tables.html")