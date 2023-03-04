from django import forms
from .models import Cartes

class ScancardForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))