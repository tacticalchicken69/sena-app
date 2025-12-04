from django.urls import path
from . import views

app_name = 'aprendices'

urlpatterns = [
    path('', views.main, name='main'),
    path('aprendices/', views.aprendices, name='lista_aprendices'),
    path("aprendices/details/<int:id>/", views.detalle_aprendiz, name="detalle_aprendiz"),
]   
