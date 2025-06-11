from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from pprint import pprint

from .models import Profesor
from .utils import profesores_ha_registrado,asignar_grupos
from tutorias.utils import periodo_actual
from tutorias.models import Periodo,TutoriaGrupal,TutoriaPares,TutoriaIndividual,TutoriaMovilidad,TutoriaRegularizacion,TutoriaRecuperacion

def test(request):
    return render(request,"responseHTML/success.html",{"saludo":"hola  mundo"})



def inicio(request):
    """ En la pantalla de inicio se hace una comprobacion de cuantas y cuales tutorías ha registrado el usuario """
    conteo_tutorias = {}
    if request.user.is_authenticated:
        tipos_tutorias = [TutoriaGrupal,TutoriaIndividual,TutoriaPares,TutoriaRegularizacion,TutoriaRecuperacion,TutoriaMovilidad]
        totales_tutorias = ["grupal","individual","pares","regularizacion","recuperacion","movilidad"]
        
        for tipo_tutoria,total_turoria in zip(tipos_tutorias,totales_tutorias):
            conteo_tutorias[total_turoria]= len(tipo_tutoria.objects.filter(tutoria__profesor=request.user))
    return render(request,"inicio.html",{"total":conteo_tutorias})

def inicio_administrador(request):
    """ En la pantalla de inicio se mostrará el numero de los usuarios que ya registraron tutorías """
    tipos_tutorias = [TutoriaGrupal,TutoriaIndividual,TutoriaPares,TutoriaRegularizacion,TutoriaRecuperacion,TutoriaMovilidad]
    totales_tutorias = ["total_grupales","total_individuales","total_pares","total_regularizacion","total_recuperacion","total_movilidad"]
    
    conteo_tutorias = {}
    """ Para cada tipo de tutoría se hara el conteo de profesores que registaron dicha tutoría """
    periodo_selecionado = request.GET.get('periodo')
    for tipo_tutoria,total_turoria in zip(tipos_tutorias,totales_tutorias):
        lista_profesores = []
        for instancia in tipo_tutoria.objects.select_related('tutoria__profesor').filter(tutoria__periodo__nombre_periodo=periodo_selecionado):
            profesor = instancia.tutoria.profesor
            if profesor not in lista_profesores:
                lista_profesores.append(profesor)
        conteo_tutorias[total_turoria] = len(lista_profesores)
    
    return render(request,"administrador.html",{
        "total_profesores": len(profesores_ha_registrado(periodo_selecionado)),
        "totales_tutorias": conteo_tutorias,
        "periodos":Periodo.objects.all(),
        "query": periodo_selecionado
    })

@login_required
def profesores(request,periodo):
    query = request.GET.get("q", "")
    profesores = profesores_ha_registrado(periodo)
    resultados = profesores.filter(nombre__icontains=query) if query else profesores
    if request.method == "GET":
        return render(request,"profesores.html",{
            "lista_profesores": resultados,
            "periodo":periodo,
            'query':query,
            "mostrar":False
        })
    tipos_tutorias = [TutoriaGrupal,TutoriaPares,TutoriaIndividual,TutoriaMovilidad,TutoriaRegularizacion,TutoriaRecuperacion]
    tt = ["grupal","pares","individual","movilidad","regularizacion","recuperacion"]
    
    profesor_seleccionado = request.POST.get("profesor_seleccionado")
    pr = Profesor.objects.get(nombre=profesor_seleccionado)
    
    tutorias_asociadas = {}
    for tutorias,t in zip(tipos_tutorias,tt):
        tutorias_asociadas[f"tutoria_{t}"]=tutorias.objects.filter(tutoria__profesor=pr)
    
    movilidad = tutorias_asociadas["tutoria_movilidad"]
    alumnos_movilidad = {}
    if movilidad:
        for alumno_m in movilidad[0].boleta_nombre.split(";"):
            boleta,nombre = alumno_m.split(",")
            alumnos_movilidad[boleta] = nombre
    return render(request,"profesores.html",{
        "lista_profesores": resultados,
        "profesor_seleccionado":profesor_seleccionado,
        "tutorias_asociadas":tutorias_asociadas,
        "alumnos_movilidad": alumnos_movilidad,
        "periodo":periodo,
        'query':query,
        "mostrar":True
    })

def reporte(request,periodo):
    """ Obtenemos todas las tutorias del periodo selecionado """    
    tutorias_flitardas = TutoriaGrupal.objects.filter(tutoria__periodo__nombre_periodo=periodo)
    """ Se consturira un diccionario con un tupla fecha-profesor como clave y una lista de sus grupos como definicion
        {
            (fecha_ultimo_registro_1, nombre_profesor_1) : [grupo_1,grupo_2,grupo_3],
            (fecha_ultimo_registro_2, nombre_profesor_2) : [grupo_1,grupo_2,grupo_3],
            ...
        }
    """
    """ Primero obtenemos la informacion del profesor con sus respectivos grupos registrados """
    primera_lista = {}
    for instancia_tutoria in tutorias_flitardas.select_related("tutoria__profesor"):
        profesor = instancia_tutoria.tutoria.profesor
        if profesor not in primera_lista:
            primera_lista[profesor] = []
        primera_lista[profesor].append(instancia_tutoria)
    """ Ahora reconstruimos el diccionario con la fecha de su ultimo grupo registrado y agregando
    una X a los grupos que le falto por registrar """
    tutorias_grupales = {}
    for profesor,grupos in primera_lista.items():
        clave = (grupos[-1].tutoria.fecha,profesor)
        tutorias_grupales[clave] = []
        for grupo in grupos:
            tutorias_grupales[clave].append(grupo.grupo)
        while len(tutorias_grupales[clave])<3:
            tutorias_grupales[clave].append("X")
    tutorias_grupales = dict(sorted(tutorias_grupales.items(), key=lambda item: item[0][0]))
    if request.method == "GET":
        return render(request,"reporte.html",{"lista_profesores":tutorias_grupales,"periodo":periodo,"mostrar":False})
    
    grupos_asignados = asignar_grupos(tutorias_grupales)
    
    for nombre, grupo in grupos_asignados:
        for clave in tutorias_grupales:  # Recorrer las claves (tuplas)
            if clave[1] == nombre:  # Comprobar si el nombre coincide
                tutorias_grupales[clave].append(grupo)
                break  # Una vez encontrado, no es necesario seguir buscando

    return render(request,"reporte.html",{
        "lista_profesores":tutorias_grupales,
        "periodo":periodo,
        "grupos_asignados":grupos_asignados,
        "mostrar":True,
    })
    
    
    
        
#ELIMINAR REGISTRO DEL PROFESOR Y SUS TUTORÍAS -------------  ----------------------------------
def eliminar_profesor(request,profesor_id):
    try:
        profesor = get_object_or_404(Profesor, id=profesor_id)
        profesor.delete()
    except:
        return render(request,"responseHTML/failure.html")

#REGISTAR USUARIO ------------------------------------------------------------------------------
def signup(request):
    if request.method == "GET":
        return render(request, "singup.html")
    try:
        if Profesor.objects.filter(email=request.POST["correo_institucional"]).exists():
            raise ValueError(f'Ya existe una cuenta asociada al correo {request.POST["correo_institucional"]}.Si usted no resgitro este usuario contacte con el administrador')
        if Profesor.objects.filter(username=request.POST["usuario"]).exists():
            raise ValueError("El nombre de usuario ya está en uso, por favor utilice otro.")
        if request.POST["password1"] != request.POST["password2"]:
            raise ValueError("Las contraseñas no coinciden")
        profesor_creado = Profesor(
            nombre = request.POST["nombre"],
            email = request.POST["correo_institucional"],
            correo_alterno = request.POST["correo_alterno"],
            username = request.POST["usuario"],
        )
        profesor_creado.set_password(request.POST["password1"])
        profesor_creado.save()
        return render(request,"responseHTML/success.html",{"success": "usuario creado"})
    except ValueError as error:
        return render(request,"singup.html", {"error": str(error)})
    except Exception as no_se:
        return render(request,"singup.html", {"error": f'Error no contemplado, intente mas tarde: {no_se}'})

#INICIAR SESIÓN --------------------------------------------------------------------------------
def signin(request):
    if request.method == "GET":
        return render(request, "login.html")
    try:
        username=request.POST['username']
        password=request.POST['password']
        if not Profesor.objects.filter(username=username).exists():
            raise ValueError("Usuario no registrado.")
        user = Profesor.objects.get(username=username)
        if not user.is_active:
            raise ValueError("Tu cuenta está inactiva. Contacta al administrador.")
        auth = authenticate(request,username=username,password=password)
        if auth is None:
            raise ValueError("Credenciales incorrectas. Intenta nuevamente")
        login(request,auth)
        if user.is_superuser:
            return redirect("administrador")
        return redirect("inicio")
    except ValueError as error:
        return render(request, "login.html", { "error": str(error) })
    except Exception as no_se:
        return render(request,"singup.html", {"error": f'Error no contemplado, intente mas tarde: {no_se}'})

#CERRAR SESIÓN ---------------------------------------------------------------------------------
@login_required
def signout(request):
    logout(request)
    return redirect("inicio")