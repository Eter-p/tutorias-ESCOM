from datetime import datetime
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.utils.timezone import now,make_aware
from django.utils.http import urlsafe_base64_decode

from .models import Profesor
from .utils import profesores_ha_registrado,asignar_grupos,enviar_correo_activacion
from tutorias.utils import periodo_actual
from tutorias.models import Periodo,TutoriaGrupal,TutoriaPares,TutoriaIndividual,TutoriaMovilidad,TutoriaRegularizacion,TutoriaRecuperacion

def inicio(request):
    """ En la pantalla de inicio se hace una comprobacion de cuantas y cuales tutorías ha registrado el usuario """
    conteo_tutorias = {}
    if request.user.is_authenticated:
        tipos_tutorias = [TutoriaGrupal,TutoriaIndividual,TutoriaPares,TutoriaRegularizacion,TutoriaRecuperacion,TutoriaMovilidad]
        nombre_tutorias = ["grupal","individual","pares","regularizacion","recuperacion","movilidad"]
        max_tutorias = [3,1,2,1,1,1]
        
        periodo = periodo_actual()
        if periodo == None:
            periodo = Periodo.objects.latest("fecha_cierre")
        for tipo_tutoria,nombre_turoria,maximo in zip(tipos_tutorias,nombre_tutorias,max_tutorias):
            conteo_tutorias[nombre_turoria]= maximo-len(tipo_tutoria.objects.filter(tutoria__profesor=request.user,tutoria__periodo=periodo))
        return render(request,"inicio.html",{"restante":conteo_tutorias,"fecha":now(),"periodo":periodo})
    return render(request,"inicio.html")

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
def listar_profesores(request,periodo):
    """ Obtenemos y filtramos todos los usuarios que ya registraron tutorías en el periodo seleccionado """
    query = request.GET.get("q", "")
    profesores = profesores_ha_registrado(periodo)
    lista_profesores = profesores.filter(nombre__icontains=query) if query else profesores
    if request.method == "GET":
        return render(request,"profesores.html",{
            "lista_profesores": lista_profesores,
            "periodo":periodo,
            'query':query,
            "mostrar_tutorias":False
        })
        
    """ Si se da clic sobre un nombre se envia un fomulario con el nombre  """
    profesor_clicado = request.POST.get("profesor_seleccionado")

    """ Obtenemos todas las tutorias relacionadas a ese profesor """
    profesor_seleccionado = Profesor.objects.get(nombre=profesor_clicado)
    tipos_tutorias = [TutoriaGrupal,TutoriaPares,TutoriaIndividual,TutoriaMovilidad,TutoriaRegularizacion,TutoriaRecuperacion]
    nombres_tutorias = ["grupal","pares","individual","movilidad","regularizacion","recuperacion"]
    tutorias_asociadas = {}
    for tutorias,nombre in zip(tipos_tutorias,nombres_tutorias):
        tutorias_asociadas[f"tutoria_{nombre}"]=tutorias.objects.filter(tutoria__profesor=profesor_seleccionado)
    
    """ Si el tipo de tutoria es de movilidad adicionalmente se enviará la infomación con un mejor formato """
    movilidad = tutorias_asociadas["tutoria_movilidad"]
    alumnos_movilidad = {}
    if movilidad:
        for alumno_m in movilidad[0].boleta_nombre.split(";"):
            boleta,nombre = alumno_m.split(",")
            alumnos_movilidad[boleta] = nombre
    
    return render(request,"profesores.html",{
        "lista_profesores": lista_profesores,
        "profesor_clicado":profesor_clicado,
        "tutorias_asociadas":tutorias_asociadas,
        "alumnos_movilidad": alumnos_movilidad,
        "periodo":periodo,
        'query':query,
        "mostrar_tutorias":True
    })

@login_required
def estadisticas(request,periodo):
    return render(request,"estadisticas.html",{"periodo":periodo})

@login_required
def get_char(request,periodo):
    conteo_tutorias = {}
    tipos_tutorias = [TutoriaGrupal,TutoriaIndividual,TutoriaPares,TutoriaRegularizacion,TutoriaRecuperacion,TutoriaMovilidad]
    nombres_tutorias = ["grupales","individuales","pares","regularizacion","recuperacion","movilidad"]
    for tipo_tutoria,nombre_tutorias in zip(tipos_tutorias,nombres_tutorias):
        lista_profesores = []
        contador_alumnos = 0
        for instancia in tipo_tutoria.objects.select_related('tutoria__profesor').filter(tutoria__periodo__nombre_periodo=periodo):
            profesor = instancia.tutoria.profesor
            if profesor not in lista_profesores:
                lista_profesores.append(profesor)
                if tipo_tutoria == TutoriaGrupal:
                    contador_alumnos = contador_alumnos + int (instancia.no_hombres_grupal) + int(instancia.no_mujeres_grupal)
            if tipo_tutoria == TutoriaIndividual:
                contador_alumnos = contador_alumnos + int (instancia.no_hombres_individual) + int(instancia.no_mujeres_individual)
            if tipo_tutoria == TutoriaPares:
                contador_alumnos = contador_alumnos + 1
            if tipo_tutoria == TutoriaRegularizacion:
                contador_alumnos = contador_alumnos + int (instancia.no_hombres_regularizacion) + int(instancia.no_mujeres_regularizacion)
            if tipo_tutoria == TutoriaRecuperacion:
                contador_alumnos = contador_alumnos + int (instancia.no_hombres_recuperacion) + int(instancia.no_mujeres_recuperacion)
            if tipo_tutoria == TutoriaMovilidad:
                contador_alumnos = contador_alumnos + int (instancia.no_hombres_movilidad) + int(instancia.no_mujeres_movilidad)
        conteo_tutorias["profesores_"+nombre_tutorias] = len(lista_profesores)
        conteo_tutorias["alumnos_"+nombre_tutorias] = contador_alumnos
    
    individales = 0
    for tutoria in TutoriaIndividual.objects.filter(tutoria__periodo__nombre_periodo=periodo):
        individales = individales + int (tutoria.no_hombres_individual) + int(tutoria.no_mujeres_individual)
        
    option_grupos = {
        "title": {
            "text": "Número de profesores que registarón tutorías",
            "subtext": f"Periodo {periodo}",
            "left": 'center',
            "textStyle":{"fontSize":20}
        },
        "tooltip": {
            "trigger": "item",
            },
        "legend": {
            "orient": 'vertical',
            "left": 'left'
        },
        "series": [{
            "type": 'pie',
            "radius": '75%',
            "data": [
                { "value": conteo_tutorias["profesores_grupales"], "name": 'Grupales'},
                { "value": conteo_tutorias["profesores_individuales"], "name": 'Individuales'},
                { "value": conteo_tutorias["profesores_pares"], "name": 'Pares'},
                { "value": conteo_tutorias["profesores_regularizacion"], "name": 'Regularización'},
                { "value": conteo_tutorias["profesores_recuperacion"], "name": 'Recuperación'},
                { "value": conteo_tutorias["profesores_movilidad"], "name": 'Movilidad'}
            ],
            "label": {
                "fontSize": 16,
                "formatter":" {b}: {c}"
            },
            "emphasis": {
                "itemStyle": {
                "shadowBlur": 10,
                "shadowOffsetX": 0,
                "shadowColor": 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    }
    
    option_alumnos = {
        "title": {
            "text": "Número de alumnos registrados",
            "subtext": f"Periodo {periodo}",
            "left": 'center',
            "textStyle":{"fontSize":20}
        },
        "tooltip": {
            "trigger": "item",
            },
        "legend": {
            "orient": 'vertical',
            "left": 'left'
        },
        "series": [{
            "type": 'pie',
            "radius": '75%',
            "data": [
                { "value": conteo_tutorias["alumnos_grupales"], "name": 'Grupales'},
                { "value": conteo_tutorias["alumnos_individuales"], "name": 'Individuales'},
                { "value": conteo_tutorias["alumnos_pares"], "name": 'Pares'},
                { "value": conteo_tutorias["alumnos_regularizacion"], "name": 'Regularización'},
                { "value": conteo_tutorias["alumnos_recuperacion"], "name": 'Recuperación'},
                { "value": conteo_tutorias["alumnos_movilidad"], "name": 'Movilidad'},
            ],
            "label": {
                "fontSize": 16,
                "formatter":" {b}: {c}"
            },
            "emphasis": {
                "itemStyle": {
                "shadowBlur": 10,
                "shadowOffsetX": 0,
                "shadowColor": 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    }
    return JsonResponse({
        "grupos": option_grupos,
        "alumnos": option_alumnos
    })

@login_required
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
        for tutoria in primera_lista[nombre]:
            if grupo == tutoria.grupo:
                tutoria.tutoria_asignada = True
                tutoria.save()
        for clave in tutorias_grupales:  
            if clave[1] == nombre:  
                tutorias_grupales[clave].append(grupo)
                break 

    return render(request,"reporte.html",{
        "lista_profesores":tutorias_grupales,
        "periodo":periodo,
        "grupos_asignados":grupos_asignados,
        "mostrar":True,
    })

@login_required
def configuracion(request):
    if request.method == "GET":
        periodos = Periodo.objects.all()
        return render(request,"settings.html",{
            "periodos":periodos,
        })
    try: 
        if "periodo_id" in request.POST:
            periodo = get_object_or_404(Periodo, id=request.POST["periodo_id"])
            nombre_nuevo = request.POST.get("nombre_periodo").strip()
            fecha_apertura = datetime.strptime(request.POST.get("fecha_apertura"), "%Y-%m-%dT%H:%M")
            fecha_cierre = datetime.strptime(request.POST.get("fecha_cierre"), "%Y-%m-%dT%H:%M")
            if not nombre_nuevo:
                raise ValueError("El nombre del periodo no puede estar vacío.")
            if fecha_apertura >= fecha_cierre:
                raise ValueError("La fecha de apertura debe ser anterior a la de cierre.")
            periodo.nombre_periodo = nombre_nuevo
            periodo.fecha_apertura = make_aware(fecha_apertura)
            periodo.fecha_cierre = make_aware(fecha_cierre)
            periodo.save()
            return render(request, "settings.html", {"periodos": Periodo.objects.all(), "msg": "Información actualizada"})
        nombre_periodo = request.POST.get("nuevo_nombre_periodo").strip()
        fecha_apertura = datetime.strptime(request.POST.get("nuevo_fecha_apertura"), "%Y-%m-%dT%H:%M")
        fecha_cierre = datetime.strptime(request.POST.get("nuevo_fecha_cierre"), "%Y-%m-%dT%H:%M")
        if not nombre_periodo:
            raise ValueError("El nombre del nuevo periodo no puede estar vacío.")
        if fecha_apertura >= fecha_cierre:
            raise ValueError("La fecha de apertura debe ser anterior a la de cierre.")
        Periodo.objects.create(
            nombre_periodo=nombre_periodo,
            fecha_apertura=make_aware(fecha_apertura),
            fecha_cierre=make_aware(fecha_cierre),
        )
        return render(request, "settings.html", {"periodos": Periodo.objects.all(), "msg": "Periodo Agregado"})
    except ValueError as e:
        return render(request, "settings.html", {"periodos": Periodo.objects.all(), "error": str(e)})

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
            is_active=False
        )
        profesor_creado.set_password(request.POST["password1"])
        profesor_creado.save()
        enviar_correo_activacion(profesor_creado)
        return render(request,"responseHTML/success.html",{"success": "usuario creado"})
    except ValueError as error:
        return render(request,"singup.html", {"error": str(error)})
    except Exception as no_se:
        return render(request,"singup.html", {"error": f'Error no contemplado, intente mas tarde.\nNOTA: Hay posibolidad de que su cuenta haya sido creada. Trate de iniciar sesión\nInformación sobre el error: {no_se}'})

def signin(request):
    if request.method == "GET":
        return render(request, "login.html")
    try:
        username=request.POST['username']
        password=request.POST['password']
        if not Profesor.objects.filter(username=username).exists():
            raise ValueError("NRegistro")
        user = Profesor.objects.get(username=username)
        if not user.is_active:
            raise ValueError("CInactiva")
        auth = authenticate(request,username=username,password=password)
        if auth is None:
            raise ValueError("Incorrecto")
        login(request,auth)
        if user.is_superuser:
            return redirect("administrador")
        return redirect("inicio")
    except ValueError as error:
        return render(request, "login.html", { "error": str(error) })
    except Exception as no_se:
        return render(request,"singup.html", {"error": f'Error no contemplado, intente mas tarde.\nInformación del error:{no_se}'})

@login_required
def signout(request):
    logout(request)
    return redirect("inicio")

def reenviar_activacion(request):
    enviar_correo_activacion(Profesor.objects.get(email=request.POST["correo"]))
    return render(request,"responseHTML/success.html",{"success":"correo reenviado"})
def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Profesor.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Profesor.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request,"responseHTML/success.html",{"success": "usuario activado"})
    else:
        return render(request, 'responseHTML/failure.html', {
            'error': 'El enlace de activación no es válido o ha expirado.'
        })