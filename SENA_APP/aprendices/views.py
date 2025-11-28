from unittest import loader
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from .models import Aprendiz    

def aprendices(request):
    lista_aprendices = Aprendiz.objects.all().values()
    template = loader.get_template("listar_aprendices.html")
    
    context = {
        "lista_aprendices": lista_aprendices,
    }
    return HttpResponse(template.render(context, request))
def detalle_aprendiz(request, aprendiz_id):
    def detalle_aprendiz(request, aprendiz_id):
    template = loader.get_template('detalle_aprendiz.html')
    
    context = {
        'aprendiz': aprendiz,
    }
    
    return HttpResponse(template.render(context, request))

def aprendices(request):
    return HttpResponse("Hello world!")