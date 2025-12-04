from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Aprendiz
from instructores.models import Instructor
from programas.models import Programa
from cursos.models import Curso 

def aprendices(request):
    lista_aprendices = Aprendiz.objects.all()
    template = loader.get_template("lista_aprendices.html")
    
    context = {
        "lista_aprendices": lista_aprendices,
    }
    return HttpResponse(template.render(context, request))


def detalle_aprendiz(request, id):
    aprendiz = Aprendiz.objects.get(id=id)
    template = loader.get_template('detalle_aprendiz.html')
    
    context = {
        'aprendiz': aprendiz,
    }
    
    return HttpResponse(template.render(context, request))

def main(request):
    template = loader.get_template("main.html")
    context = {
        'total_aprendices': Aprendiz.objects.count(),
        'total_instructores': Instructor.objects.count(),
        'total_programas': Programa.objects.count(),
        'total_cursos': Curso.objects.count(),
        'cursos_activos': Curso.objects.filter(estado='EJE').count(),
    }
    return HttpResponse(template.render(context, request))