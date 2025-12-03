from django.urls import path
from . import views

app_name = 'programas'

urlpatterns = [
    
    path('', views.programas, name='lista_programas'),
    path('programas/<int:id_programas>/', views.detalle_programa, name='detalle_programas'),
]