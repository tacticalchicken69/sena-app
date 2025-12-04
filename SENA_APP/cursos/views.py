from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Curso

# Create your views here.

def cursos(request):
    lista_cursos = Curso.objects.all()
    template = loader.get_template("lista_cursos.html")
    context = {
        "lista_cursos": lista_cursos,
    }
    return HttpResponse(template.render(context, request))


def detalle_curso(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    template = loader.get_template("detalle_cursos.html")
    # calcular cupos disponibles y ocupacion si se desea
    try:
        cupos_disponibles = curso.cupos_maximos - curso.aprendices.count()
    except Exception:
        cupos_disponibles = None

    context = {
        "curso": curso,
        "cupos_disponibles": cupos_disponibles,
        "instructores_count": curso.instructores.count() if hasattr(curso, 'instructores') else 0,
        "aprendices_count": curso.aprendices.count() if hasattr(curso, 'aprendices') else 0,
    }
    return HttpResponse(template.render(context, request))
