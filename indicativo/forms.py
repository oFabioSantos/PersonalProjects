from .models import Indicativos, RadioAmador, Conversa
from django import forms

class indicativosForm(forms.ModelForm):
    """Form baseado no model da aplicação"""
    
    class Meta:
        model = Indicativos
        fields = ['nome']  #  O nome dentro do array deve ser o mesmo dos atributos da classe
        labels = {'nome': ''}
        

class RadioAmadorForms(forms.ModelForm):
    """Form baseado no model da aplicação"""
    
    class Meta:
        model = RadioAmador
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'col': 80})}      
        

class ConversaForms(forms.ModelForm):
    """Form baseado no model Conversa/QSO"""
    
    class Meta:
        model = Conversa
        fields = ['text'] 
        labels = {'text': ''} 
        widgets = {'text': forms.Textarea(attrs={'col': 80})}      