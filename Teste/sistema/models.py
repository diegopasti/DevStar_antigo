import datetime
from decimal import Decimal
import re
import time
import urllib2  # ,re,smtplib

from bs4 import BeautifulSoup
from django import forms
from django.db import models
from django.db.models.aggregates import Max, Avg


class Projeto(models.Model):
    
    Nome      = models.CharField(max_length=100,null=False,unique=False)
    ProjetoUsuario = models.BooleanField(default=False)  
    Linguagem = models.CharField(max_length=50,null=True,unique=False) 
    Link      = models.CharField(max_length=100,null=False,unique=True)
    Atualizado = models.BooleanField(default=False)

def CalcularNota(estado):
    complexidade = float(estado.ComplexidadePorMetodo)
    piorComplexidade = float(PiorValor('ComplexidadePorMetodo'))
    notaComplexidade = round(100.0-((100.0*(complexidade-1))/piorComplexidade),2)
    
    duplicacao = float(estado.TaxaDuplicacao)
    piorDuplicacao = float(PiorValor('TaxaDuplicacao'))
    notaDuplicacao = round(100.0-((100.0*(duplicacao))/piorDuplicacao),2)
    
    divida = float(estado.TaxaDividaTecnica)
    piorDivida = float(PiorValor('TaxaDividaTecnica'))
    notaDivida = round(100.0-((100.0*(divida))/piorDivida),2)
    
    #print "nota: ",notaComplexidade," > ",duplicacao,"/",piorDuplicacao
    #print "nota: ",notaDuplicacao," > ",duplicacao,"/",piorDuplicacao
    #print "nota: ",notaDivida," > ",divida,"/",piorDivida
    
    notafinal = round(notaComplexidade*0.4+notaDuplicacao*0.3+notaDivida*0.3)/10
    #print "Nota Final: ",notafinal
    return notafinal

def PiorValor(coluna):
    valor = round(Estado.objects.all().aggregate(Max(coluna))[coluna+'__max'],2)
    return valor

def ValorMedio(coluna):
    valor = round(Estado.objects.all().aggregate(Avg(coluna))[coluna+'__avg'],2)
    return valor
    

class Estado(models.Model):
    Data = models.DateTimeField(auto_now_add=True)
    Projeto = models.ForeignKey(Projeto)
    
    NumeroLinhasCodigo     = models.IntegerField(null=True,default=None)
    NumeroTotalLinhas      = models.IntegerField(null=True,default=None)
    NumeroClasses          = models.IntegerField(null=True,default=None)
    NumeroArquivos         = models.IntegerField(null=True,default=None)
    NumeroMetodos          = models.IntegerField(null=True,default=None)
    
    ComplexidadeTotal      = models.DecimalField(max_digits=10, decimal_places=2,null=True,default=None)
    ComplexidadePorMetodo  = models.DecimalField(max_digits=4, decimal_places=2,null=True,default=None)
    ComplexidadePorClasse  = models.DecimalField(max_digits=7, decimal_places=2,null=True,default=None)
    ComplexidadePorArquivo = models.DecimalField(max_digits=10, decimal_places=2,null=True,default=None)
    
    TaxaDuplicacao           = models.DecimalField(max_digits=4, decimal_places=2,null=True,default=None)
    TaxaDuplicacaoPorTamanho = models.DecimalField(max_digits=4, decimal_places=2,null=True,default=None)
    
    NumeroProblemasTotais            = models.IntegerField(null=True,default=None)
    TaxaProblemasTotaisPorTamanho    = models.DecimalField(max_digits=4, decimal_places=2,null=True,default=None)
    TaxaDividaTecnica                = models.DecimalField(max_digits=4, decimal_places=2,null=True,default=None)
    TaxaDividaTecnicaPorTamanho      = models.DecimalField(max_digits=4, decimal_places=2,null=True,default=None)
    
    NumeroProblemasMuitoCriticos = models.IntegerField(null=True,default=None)
    NumeroProblemasCriticos      = models.IntegerField(null=True,default=None)
    NumeroProblemasModerados     = models.IntegerField(null=True,default=None)
    NumeroProblemasNormais       = models.IntegerField(null=True,default=None)
    NumeroProblemasSimples       = models.IntegerField(null=True,default=None)
    
    ProblemasMuitoCriticosPorTamanho = models.DecimalField(max_digits=4, decimal_places=2,null=True,default=None)
    ProblemasCriticosPorTamanho      = models.DecimalField(max_digits=4, decimal_places=2,null=True,default=None)
    ProblemasModeradosPorTamanho     = models.DecimalField(max_digits=4, decimal_places=2,null=True,default=None)
    ProblemasNormaisPorTamanho       = models.DecimalField(max_digits=4, decimal_places=2,null=True,default=None)
    ProblemasSimplesPorTamanho       = models.DecimalField(max_digits=4, decimal_places=2,null=True,default=None)
    
    Nota = models.DecimalField(max_digits=5,decimal_places=2,null=True,default=None)
    
class Categoria(models.Model):
    Nome = models.CharField(max_length=50)
    #Estado = Estado
    
class Metrica(): 

    Nome         = None
    MelhorValor  = None
    ValorMedio   = None
    ValorMediano = None
    PiorValor    = None
    Meta         = None



    
class VerificadorProjetos():
    
    Arquivo    = None
    LeitorHTML = None
    Projeto    = None    
    
    def __init__(self,*args):
        print "Verificador Construido com Sucesso! \n"
        
    def BuscarInformacaoBasica(self,link):
        self.BaixarArquivo(link)
        self.SimplificarDocumento()
        return self.getNomeProjeto(),self.getLinguagemProjeto()
    
    def Analisar(self,Projeto):
        self.BaixarArquivo(Projeto.Link)
        self.SimplificarDocumento()
        
        estado_projeto = Estado()
        estado_projeto.Projeto = Projeto
          
        estado_projeto.NumeroLinhasCodigo     = self.getMetrica("m_ncloc", "block_1")
        estado_projeto.NumeroTotalLinhas      = self.getMetrica("m_lines", "block_1")
        estado_projeto.NumeroClasses          = self.getMetrica("m_classes", "block_1")
        estado_projeto.NumeroArquivos         = self.getMetrica("m_files", "block_1")
        estado_projeto.NumeroMetodos          = self.getMetrica("m_functions", "block_1")
        
        estado_projeto.ComplexidadeTotal      = self.getMetrica("m_complexity", "block_3")
        estado_projeto.ComplexidadePorMetodo  = self.getMetrica("m_function_complexity", "block_3")
        estado_projeto.ComplexidadePorClasse  = self.getMetrica("m_class_complexity", "block_3")
        estado_projeto.ComplexidadePorArquivo = self.getMetrica("m_file_complexity", "block_3")
        
        estado_projeto.TaxaDuplicacao = self.getMetrica("m_duplicated_lines_density","block_437","block_2")
        
        estado_projeto.TaxaDividaTecnica            = self.getMetrica("m_sqale_debt_ratio","block_616","block_6")
        estado_projeto.NumeroProblemasMuitoCriticos = self.getMetrica("m_blocker_violations","block_7")
        estado_projeto.NumeroProblemasCriticos      = self.getMetrica("m_critical_violations","block_7")
        estado_projeto.NumeroProblemasModerados     = self.getMetrica("m_major_violations","block_7")
        estado_projeto.NumeroProblemasNormais       = self.getMetrica("m_minor_violations","block_7")
        estado_projeto.NumeroProblemasSimples       = self.getMetrica("m_info_violations","block_7")
        
        return estado_projeto
        

    def AnalisarProjeto(self,link):
        self.BaixarArquivo(link)
        self.SimplificarDocumento()
        
        self.Projeto               = Projeto(link)
        self.Projeto.Nome          = self.getNomeProjeto()
        self.Projeto.Complexidade  = self.getMetrica("m_function_complexity", "block_3")
        self.Projeto.Duplicacao    = self.getMetrica("m_duplicated_lines_density","block_437","block_2")
        self.Projeto.DividaTecnica = self.getMetrica("m_sqale_debt_ratio","block_616")
        
        texto = "" + "Projeto: "+self.Projeto.Nome+"\n"
        texto = texto + "Complexidade: "+self.Projeto.Complexidade+"\n"
        texto = texto + "Duplicacao: "+self.Projeto.Duplicacao+"\n"
        texto = texto + "Divida Tecnica: "+self.Projeto.DividaTecnica+"\n"
         
        return texto
        
    def getTotalNemoLinks(self):
        self.BaixarArquivo("http://nemo.sonarqube.org/measures/search/68?widget_id=&asc=false&c3_metric=tests&c3_op=eq&cols%5B%5D=metric%3Aalert_status&cols%5B%5D=name&cols%5B%5D=date&cols%5B%5D=metric%3Ancloc&cols%5B%5D=metric%3Aviolations&cols%5B%5D=links&display=list&page=1&pageSize=100&qualifiers%5B%5D=TRK&sort=metric%3Ancloc&id=68")
        self.SimplificarDocumento()
                
        div = self.Arquivo.findAll("div", id="measure_filter_foot_pages")[0].contents[0]
        div = str(div)
        
        resultado = re.search(r'^>*(\d*) results', div).group(1)
        return int(resultado)
            
    def getNemoLinks(self):
        Links = []
        Fonte, Lista = self.getLinks("http://nemo.sonarqube.org/measures/search/68?widget_id=&asc=false&c3_metric=tests&c3_op=eq&cols%5B%5D=metric%3Aalert_status&cols%5B%5D=name&cols%5B%5D=date&cols%5B%5D=metric%3Ancloc&cols%5B%5D=metric%3Aviolations&cols%5B%5D=links&display=list&page=1&pageSize=100&qualifiers%5B%5D=TRK&sort=metric%3Ancloc&id=68")
        Links = Links+Lista
        
        while Fonte != None:
            Fonte, Lista = self.getLinks(Fonte)
            Links = Links+Lista
        return Links              
        
    def getLinks(self,Fonte):
        Links = []
        self.BaixarArquivo(Fonte)
        self.SimplificarDocumento()
                
        div = self.Arquivo.findAll("td",{"class":"nowrap"})
                
        for item in div:
            link = item.findAll("a",href=True,title=True)
            if link != []:  
                Links.append("http://nemo.sonarqube.org"+link[0]['href'])
                #print "Adicionando link: ","http://nemo.sonarqube.org"+link[0]['href']
                
        footer = self.Arquivo.find("tfoot")
       
        list_links = footer.findAll("a",href=True)
        
        url = None
        for link in list_links:
            if "Next" in link:                
                url = "http://nemo.sonarqube.org"+link["href"]
               
        return url,Links
        
    
    def BaixarArquivo(self,link):
        Conexao = urllib2.urlopen(link)
        self.Arquivo = Conexao.read()
        
    def SimplificarDocumento(self):
        self.LeitorHTML = BeautifulSoup(self.Arquivo,"html5lib")
        self.Arquivo = self.LeitorHTML.find('div',{'id':'body'})
    
    def getMetrica(self,metrica_id,block_id_padrao,*args):
        #inicio = time.time()
        try:
            valor = self.Arquivo.find("span",id=metrica_id).contents[0]
            valor = valor.replace(",","")
            valor = valor.replace("%","")
            
        except:
            print "Algum valor nao foi encontrado e foi definido com Zero"
            valor = 0
        
        #duracao = time.time() - inicio
        #print "Consulta em ",duracao
        return valor
        #try:
        """
        div = self.Arquivo.find("div",{"class":"block","id":block_id_padrao})
        if div == None:
            print "A metrica: ",block_id_padrao," Falha! Veja o valor: (",div,") acho que nao tem um id_extra pra procurar.. ve ae: ",args 
            div = self.Arquivo.find("div",{"class":"block","id":args[0]})
            print "A metrica: ",block_id_padrao," Falha! Veja o valor: (",div,")"
        
        try:
            valor = div.find("span",id=metrica_id).contents[0]
            valor = valor.replace(",","")
            valor = valor.replace("%","")
            return valor
        except:
            return None
        """
         
    
    def getLinguagemProjeto(self):
        try:
            valor = self.Arquivo.findAll("table",id="size-widget-language-dist")[0].findAll(['td'])[0].contents[0]
        except:
            try:
                div = self.Arquivo.find("div",{"class":"block","id":"block_1"})
                valor = div.find("div",{"class":"widget-measure-container"})
                valor = valor.contents[2]
            except:
                return None               
        
        if valor[0] == " ": 
            valor = valor[1:]
            
        valor = valor.replace("\n","")  
        return valor 
            
    def getNomeProjeto(self):
        divs = self.Arquivo.findAll("div",id="block_112")
        try:
            if divs != None:
                nome = divs[0].findAll(['h3'])[0].contents[2]
        except:
            divs = self.Arquivo.find('div',{'class':'print'})
            nome = divs.find('h2').contents[0]
            
        
        if nome[0] == " ": 
            nome = nome[1:]
            
        nome = nome.replace("\n","")
        return nome

     
