# -*- encoding: utf-8 -*-
from django import forms

class SearchForm(forms.Form):
    Título = forms.CharField(required=False)
    Precio = forms.FloatField(required=False)
    Graduación = forms.FloatField(required=False)
    Procedencia = forms.CharField(required=False)
    Categoría = forms.CharField(required=False)

    
