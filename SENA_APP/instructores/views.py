from unittest import loader
from django.shortcuts import render

def instructores(request):
    lista_instructores = Instructor.objects.all().values()
    template = loader.get_template("listar_instructores.html")
    
    context = {
        "lista_instructores": lista_instructores,
    }
    return HttpResponse(template.render(context, request))