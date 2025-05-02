from django.shortcuts import render
from formulario.models import Profesor
from .models import TutoriaGrupal,TutoriaIndividual,TutoriaPares,TutoriaRecuperacion,TutoriaMovilidad,TutoriaRegularizacion

def lista_tutorias(request,tipo):
    if tipo == "grupal":
        tipo_tutoria = TutoriaGrupal
        template = "grupales.html"
    elif tipo == "pares":
        tipo_tutoria = TutoriaPares
        template = "pares.html"
    elif tipo == "individual":
        tipo_tutoria = TutoriaIndividual
        template = "individual.html"
    elif tipo == "movilidad":
        tipo_tutoria = TutoriaMovilidad
        template = "movilidad.html"
    elif tipo == "recuperacion":
        tipo_tutoria = TutoriaRecuperacion
        template = "recuperacion.html"
    elif tipo == "regularizacion":
        tipo_tutoria = TutoriaRegularizacion
        template = "regularizacion.html"

    query = request.GET.get("q", "")
    resultados = Profesor.objects.filter(nombre__icontains=query) if query else Profesor.objects.all()
    lista_profesores = {}
    tipo_tutoria
    for instancia in tipo_tutoria.objects.select_related('tutoria__profesor'):
        profesor = instancia.tutoria.profesor
        if (resultados.filter(nombre=profesor).exists()):
            if profesor not in lista_profesores:
                lista_profesores[profesor] = []
            lista_profesores[profesor].append(instancia)

    return render(request,template,{
        "lista_profesores": lista_profesores,
        'query':query
	})
    