import threading

from django.http.response import HttpResponse  # , HttpResponseRedirect
from django.shortcuts import render_to_response  # , redirect
from django.template.context import RequestContext

from sistema.formularios import FormularioLinkProjeto
from sistema.models import VerificadorProjetos, Projeto
from django.shortcuts import redirect


def index(request):
    return render_to_response("index.html")

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


"""
class LocalizarLinkProjetosNemo(threading.Thread):
    
    def run(self):
        lista_links = VerificadorProjetos().getNemoLinks()
        print "Consulta Concluida (",len(lista_links)," Links Encontrados)"
        
        #return render_to_response("index.html")

class LocalizarNumeroProjetosNemo(threading.Thread):
    
    def run(self):
        total = VerificadorProjetos().getTotalNemoLinks()
        
        print "Consulta Concluida (",total," Projetos Disponiveis)"
        return 
    

        #return render_to_response("cadastrar-projetos-nemo.html",{'num_links':len(lista_links),'lista_links':lista_links})
"""

#def lista(request):
#    lista_itens = ItemAgenda.objects.all()
#    return render_to_response("lista.html",{'lista_itens':lista_itens})

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


def projetos(request):
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