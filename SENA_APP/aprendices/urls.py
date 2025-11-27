from django.urls import path
from . import views
urlpatterns = [
    path('', views.main, name='main'),
    path('aprendices/', views.aprendices, name='aprendices'),
    path("aprendices/details/<int:id>/", views.details, name="details"),
]   
