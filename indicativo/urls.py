from django.urls import path
from .import views


app_name = 'indicativo'
urlpatterns = [
   
    # Home page
    path('', views.index, name='index'),
    path('listar/', views.listar_indicativos, name='listar_indicativos'),
    path('radioamador/<int:id_radioamador>', views.listar_radioamador, name='listar_radioamador'),
    path('novo_indicativo/', views.adicionar_indicativo, name='adicionar_indicativo'),
    path('nova_entrada/<int:id_radioamador>', views.adicionar_entrada, name='adicionar_entrada'),
    path('editar_dados/<int:id_radioamador>', views.editar_dados, name='editar_dados'),
    path('iniciar_qso/', views.iniciar_qso, name='iniciar_qso'),
    path('listar_qso/', views.listar_qso, name='listar_qso'),
    path('buscar_indicativos/', views.buscar_indicativos, name='buscar_indicativos'),
    
]