from django.http import HttpResponse
from django.template import loader
from .models import Programa

# Create your views here.

def main(request):
    template = loader.get_template("main.html")
    return HttpResponse(template.render())

def programas(request):
    lista_programas = Programa.objects.all().values()
    template = loader.get_template("lista_programas.html")
    context = {
        "lista_programas": lista_programas,
    }
    return HttpResponse(template.render(context, request))


def detalle_programa(request, programa_id):
    programa_detalle = Programa.objects.get(id=programa_id)
    template = loader.get_template("programa_detalle.html")
    context = {
        "programa_detalle": programa_detalle,
    }
    return HttpResponse(template.render(context, request))