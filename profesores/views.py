from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from pprint import pprint

from django.core.mail import send_mail
from django.shortcuts import render,redirect,get_object_or_404
from .models import Profesor
from tutorias.models import TutoriaGrupal,TutoriaPares,TutoriaIndividual,TutoriaMovilidad,TutoriaRegularizacion,TutoriaRecuperacion

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
        # pprint(conteo_tutorias)
    return render(request,"inicio.html",{"total":conteo_tutorias})

def inicio_administrador(request):
    if request.method == "GET":
        return render(request,"administrador.html")
    
    tipos_tutorias = [TutoriaGrupal,TutoriaPares,TutoriaIndividual,TutoriaMovilidad,TutoriaRegularizacion,TutoriaRecuperacion]
    totales_tutorias = ["total_grupales","total_individuales","total_pares","total_regularizacion","total_recuperacion","total_movilidad"]
    
    conteo_tutorias = {}
    
    for tipo_tutoria,total_turoria in zip(tipos_tutorias,totales_tutorias):
        lista_profesores = []
        for instancia in tipo_tutoria.objects.select_related('tutoria__profesor'):
            profesor = instancia.tutoria.profesor
            if profesor not in lista_profesores:
                lista_profesores.append(profesor)
        conteo_tutorias[total_turoria] = len(lista_profesores)
        
    return render(request,"administrador.html",{
        "total_profesores": len(User.objects.all()),
        "totales_tutorias": conteo_tutorias
    })

@login_required
def profesores(request):
    query = request.GET.get("q", "")
    resultados = User.objects.filter(nombre__icontains=query) if query else User.objects.all()
    if request.method == "GET":
        return render(request,"profesores.html",{
            "lista_profesores": resultados,
            'query':query,
            "mostrar":False
        })
    tipos_tutorias = [TutoriaGrupal,TutoriaPares,TutoriaIndividual,TutoriaMovilidad,TutoriaRegularizacion,TutoriaRecuperacion]
    tt = ["grupal","pares","individual","movilidad","regularizacion","recuperacion"]
    
    profesor_seleccionado = request.POST.get("profesor_seleccionado")
    pr = User.objects.get(nombre=profesor_seleccionado)
    
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
        'query':query,
        "mostrar":True
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


def enviar_correo(id,tipo,correo):
	asunto = tipo
	mensaje = "Guarda este numero en caso de necesitarlo: "+str(id)
	destinatario = correo
	send_mail(
		asunto,
		mensaje,
		'hernandez.hernandez.fabian@gmail.com',  # Desde este correo
		[destinatario],  # A este correo
		fail_silently=False,
	)
