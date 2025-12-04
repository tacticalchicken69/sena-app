from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    path('cursos/', views.cursos, name='lista_cursos'),
    path('cursos/<int:curso_id>/', views.detalle_curso, name='detalle_cursos'),
]
