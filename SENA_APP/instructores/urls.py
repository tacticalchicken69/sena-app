from django.urls import path
from . import views

app_name = 'instructores'

urlpatterns = [
    path('', views.main, name='main'),
    path('instructores/', views.instructores, name='lista_instructores'),
    path("instructores/details/<int:id_instructor>/", views.detalle_instructor, name="detalle_instructor"),
]   
