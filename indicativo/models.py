from django.db import models
from django.contrib.auth.models import User


#  O elemento mais alto da hierarquia é relacionado a classe User, os associados acompanharão o relacionamento.
class Indicativos(models.Model):
    """Representação dos indicativos de rádio"""
    
    nome = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'Indicativos'

    def __str__(self):
        return self.nome[:20]
    
    
class RadioAmador(models.Model):
    """Representação dos dados do radioamador"""
    
    indicativo = models.ForeignKey(Indicativos, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Radioamadores'
        
    def __str__(self):
        return self.text[:50]      
    

class Conversa(models.Model):
    """Representação de um QSO entre os radioamadores"""
    
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Conversas"
        
    def __str__(self):
        return self.text[:50]            
        
      
    
    
    
    
    
    
    