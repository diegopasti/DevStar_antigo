'''
Created on 28 de jul de 2015

@author: Diego
'''

from django import forms
from sistema.models import Projeto

class FormularioLinkProjeto(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ('Link',)       
        widgets = {
            'Link': forms.TextInput(attrs={'placeholder': 'Url do Projeto..','class':"form-control" }),
            }