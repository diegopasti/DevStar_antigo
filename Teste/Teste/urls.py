"""Teste URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', "sistema.views.index"),
    url(r'^cadastro_fontes/$',"sistema.views.cadastro_fontes"),
    url(r'^projeto/(?P<projeto_id>\d+)/$',"sistema.views.projeto"),
    url(r'^meus_projetos/$',"sistema.views.meus_projetos"),
    url(r'^cadastro_projetos/$',"sistema.views.cadastro_projetos"),
    url(r'^analisar_projetos/$',"sistema.views.analisar_projetos"),
    url(r'^cadastrar-projetos-nemo/$',"sistema.views.cadastrar_projetos_nemo"),
    url(r'^atualizar_barra_progresso_analise/$',"sistema.views.atualizar_barra_progresso_analise"),
    url(r'^atualizar_barra_progresso/(?P<num_links>\d+)/$',"sistema.views.atualizar_barra_progresso"),
    #url(r'^atualizar_barra_progresso/$',"sistema.views.atualizar_barra_progresso"),
]
