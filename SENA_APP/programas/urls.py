from django.urls import path
from . import views

app_name = 'programas'

urlpatterns = [
    path('programas/', views.programas, name='lista_programas'),
    path('programas/<int:programa_id>/', views.detalle_programa, name='detalle_programas'),
]