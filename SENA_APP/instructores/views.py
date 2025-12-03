from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Instructor

# Create your views here.   
def main(request):
    template = loader.get_template("main.html")
    return HttpResponse(template.render())
def instructores(request):
    lista_instructores = Instructor.objects.all()
    template = loader.get_template("lista_instructores.html")
    
    context = {
        "lista_instructores": lista_instructores,
        'total_instructores': lista_instructores.count(),
    }
    return HttpResponse(template.render(context, request))

def detalle_instructor(request, id_instructor):
    instructor = Instructor.objects.get(id=id_instructor)
    template = loader.get_template('detalle_instructor.html')
    context = {
        'instructor': instructor,
    }
    return HttpResponse(template.render(context, request))