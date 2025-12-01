from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Aprendiz 

def aprendices(request):
    lista_aprendices = Aprendiz.objects.all().values()
    template = loader.get_template("lista_aprendices.html")
    
    context = {
        "lista_aprendices": lista_aprendices,
    }
    return HttpResponse(template.render(context, request))


def detalle_aprendiz(request, aprendiz_id):
    aprendiz = Aprendiz.objects.get(id=aprendiz_id)
    template = loader.get_template('detalle_aprendiz.html')
    
    context = {
        'aprendiz': aprendiz,
    }
    
    return HttpResponse(template.render(context, request))

def main(request):
    template = loader.get_template("main.html")
    return HttpResponse(template.render())