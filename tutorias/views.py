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
    tutorias_filtradas = flitrar_datos(request,tipo_tutoria)

    alumnos_movilidad = {}
    lista_profesores = {}
    for instancia in tutorias_filtradas:
        profesor = instancia.tutoria.profesor
        if (resultados.filter(nombre=profesor).exists()):
            if profesor not in lista_profesores:
                lista_profesores[profesor] = []
            lista_profesores[profesor].append(instancia)

            if tipo_tutoria == TutoriaMovilidad:
                boletas_alumnos = {}
                for boleta_alumno in instancia.boleta_nombre.split(";"):
                    boleta,alumno = boleta_alumno.split(",")
                    boletas_alumnos[boleta] = alumno
                alumnos_movilidad[profesor] = boletas_alumnos
    
    
    return render(request,template,{
        "lista_profesores": lista_profesores,
        'carreras_check' : request.POST.getlist("carreras"),
        'query':query,
        "alumnos_movilidad":alumnos_movilidad,
        "lista": ["x1","x2","x3"]
	})

def flitrar_datos(request,tipo_tutoria):
    tutorias_filtradas = tipo_tutoria.objects.select_related('tutoria__profesor')
    if request.method == "POST":
        carreras_seleccionadas = request.POST.getlist("carreras")
        if carreras_seleccionadas:
            if tipo_tutoria == TutoriaGrupal:
                tutorias_filtradas = tutorias_filtradas.filter(carrera=carreras_seleccionadas[0])
            elif tipo_tutoria == TutoriaRegularizacion:
                tutorias_filtradas = tutorias_filtradas.filter(carrera_regularizacion=carreras_seleccionadas[0])
            elif tipo_tutoria == TutoriaRecuperacion:
                tutorias_filtradas = tutorias_filtradas.filter(carrera_recuperacion=carreras_seleccionadas[0])
            carreras_seleccionadas.pop(0)
            for carrera in carreras_seleccionadas:
                if tipo_tutoria == TutoriaGrupal:
                    tutorias_filtradas = tutorias_filtradas | tipo_tutoria.objects.select_related('tutoria__profesor').filter(carrera=carrera)
                elif tipo_tutoria == TutoriaRegularizacion:
                    tutorias_filtradas = tutorias_filtradas | tipo_tutoria.objects.select_related('tutoria__profesor').filter(carrera_regularizacion=carrera)
                elif tipo_tutoria == TutoriaRecuperacion:
                    tutorias_filtradas = tutorias_filtradas | tipo_tutoria.objects.select_related('tutoria__profesor').filter(carrera_recuperacion=carrera)
    return tutorias_filtradas
    