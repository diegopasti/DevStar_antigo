import re
import urllib2  # ,re,smtplib

from bs4 import BeautifulSoup
from django import forms
from django.db import models


class Projeto(models.Model):
    
    Nome      = models.CharField(max_length=100,null=False,unique=True)  
    Linguagem = models.CharField(max_length=50,null=True,unique=False) 
    Link      = models.CharField(max_length=100,null=False,unique=True)
    
class Estado(models.Model):
    Data                   = models.DateField()
    Hora                   = models.TimeField()
    
    NumeroLinhasCodigo     = models.IntegerField()
    NumeroClasses          = models.IntegerField()
    NumeroArquivos         = models.IntegerField()
    
    ComplexidadeTotal      = models.DecimalField(max_digits=10, decimal_places=2)
    ComplexidadePorMetodo  = models.DecimalField(max_digits=4, decimal_places=2)
    ComplexidadePorClasse  = models.DecimalField(max_digits=7, decimal_places=2)
    ComplexidadePorArquivo = models.DecimalField(max_digits=10, decimal_places=2)
    
    TaxaDuplicacao           = models.DecimalField(max_digits=4, decimal_places=2)
    TaxaDuplicacaoPorTamanho = models.DecimalField(max_digits=4, decimal_places=2)
    
    NumeroProblemasTotais            = models.IntegerField()
    TaxaProblemasTotaisPorTamanho    = models.DecimalField(max_digits=4, decimal_places=2)
    TaxaDividaTecnica                = models.DecimalField(max_digits=4, decimal_places=2)
    TaxaDividaTecnicaPorTamanho      = models.DecimalField(max_digits=4, decimal_places=2)
    
    NumeroProblemasMuitoCriticos = models.IntegerField()
    NumeroProblemasCriticos      = models.IntegerField()
    NumeroProblemasModerados     = models.IntegerField()
    NumeroProblemasNormais       = models.IntegerField()
    NumeroProblemasSimples       = models.IntegerField()
    
    ProblemasMuitoCriticosPorTamanho = models.DecimalField(max_digits=4, decimal_places=2)
    ProblemasCriticosPorTamanho      = models.DecimalField(max_digits=4, decimal_places=2)
    ProblemasModeradosPorTamanho     = models.DecimalField(max_digits=4, decimal_places=2)
    ProblemasNormaisPorTamanho       = models.DecimalField(max_digits=4, decimal_places=2)
    ProblemasSimplesPorTamanho       = models.DecimalField(max_digits=4, decimal_places=2)
    
    
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

    def AnalisarProjeto(self,link):
        self.BaixarArquivo(link)
        self.SimplificarDocumento()
        self.Projeto = Projeto(link)
        self.Projeto.Nome = self.getNome()
        self.Projeto.Complexidade = self.getComplexidade()
        self.Projeto.Duplicacao = self.getDuplicacao()
        self.Projeto.DividaTecnica = self.getDividaTecnica()
        self.Projeto.ExibirDados()
    
        
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
    
    def getMetrica(self,metrica_id,block_id_padrao,block_id_extra):
        try:
            div = self.Arquivo.find("div",{"class":"block","id":block_id_padrao})
            if div == None:
                div = self.Arquivo.find("div",{"class":"block","id":block_id_extra})
            
            valor = div.find("span",id=metrica_id)
            return valor.contents[0]
        except:
            return None 
    
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
        """
        try:
            divs = self.Arquivo.findAll("div",id="block_112")
            if divs != None:
                nome = divs[0].findAll(['h3'])[0].contents[2]
            else:
                divs = self.Arquivo.find('div',{'class':'print'})
                nome = divs.find('h2').contents[0]
            
            if nome[0] == " ": 
                nome = nome[1:]
                
            nome = nome.replace("\n","")            
            return nome
        except:
            return None
        """
        
     
