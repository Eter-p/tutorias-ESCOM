from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404

from django.core.mail import send_mail
from django.shortcuts import render,redirect,get_object_or_404
from .forms import FormProfesor
from .models import Profesor
from .utils import falta_datos,listar_alumnos
from tutorias.models import Tutorias,TutoriaGrupal,TutoriaPares,TutoriaIndividual,TutoriaMovilidad,TutoriaRegularizacion,TutoriaRecuperacion

def administrador(request):
    return render(request,"administrador.html")

#REGISTRO DEL PROFESOR Y SUS TUTORÍAS ----------------------------------------------------------
def formulario(request):
    if request.method== "GET":
        return render(request,"formulario.html")
    try:
#-------------------------------------------------------------------------------------------
#------ GUARDAR INFORMACIÓN DEL PROFESOR ---------------------------------------------------
        form = FormProfesor(request.POST)
        if not form.is_valid():
            print(form.errors)
            messages.error(request, "Entrada no valida en la sección: Profesor")
            return render(request,"formulario.html",{"error":form.errors})
        profesor_form = form.save()
        tutorias_registradas = request.POST.getlist("botonesTutoria")
#-------------------------------------------------------------------------------------------
#------ GUARDAR TUTORÍAS GRUPALES ----------------------------------------------------------
        if tutorias_registradas[0]=="ocultar":
            grupos = request.POST.getlist("grupo")
            unidades = request.POST.getlist("unidad")
            carreras = request.POST.getlist("carrera")
            hombres = request.POST.getlist("numero_hombres_grupal")
            mujeres = request.POST.getlist("numero_mujeres_grupal")
            archivos = request.POST.getlist("lista_alumnos_grupal")
            
            if falta_datos([grupos,unidades,hombres,mujeres,archivos]):
                eliminar_profesor(request,profesor_form.id)
                messages.error(request, "Faltaron campos por llenar. Revisa los campos en la sección: Tutoría Grupal.")
                return render(request,"formulario.html",{"tipo":"falta_datos"})
            
            for i in [0,1,2]:
                if grupos[i]:
                    tutoria = Tutorias.objects.create(
                        tipo = "Grupal",
                        profesor = profesor_form
                    )
                    tutoria.save()
                    tuto_grupal = TutoriaGrupal.objects.create(
                        tutoria = tutoria,
                        grupo = grupos[i],
                        unidad_aprendizaje = unidades[i],
                        carrera = carreras[i],
                        no_hombres_grupal = hombres[i],
                        no_mujeres_grupal = mujeres[i],
                        lista_alumnos_grupal = archivos[i],
                    )
                    tuto_grupal.save()
#-------------------------------------------------------------------------------------------
#------ GUARDAR TUTORÍAS ENTRE PARES -------------------------------------------------------
        if tutorias_registradas[1]=="ocultar":
            alumnos_asesores = request.POST.getlist("nombre_alumno_asesor")
            boletas_asesores = request.POST.getlist("boleta_alumno_asesor")
            unidades_asesores = request.POST.getlist("unidad_aprendizaje_pares")
            
            if falta_datos([alumnos_asesores,boletas_asesores,unidades_asesores]):
                eliminar_profesor(request,profesor_form.id)
                messages.error(request, "Faltaron campos por llenar. Revisa los campos en la sección: Tutoria entre pares.")
                return render(request,"formulario.html",{"tipo":"falta_datos"})
            
            for i in [0,1]:
                if alumnos_asesores[i]:
                    tutoria = Tutorias.objects.create(
                        tipo = "Pares",
                        profesor = profesor_form
                    )
                    tutoria.save()
                    tuto_pares = TutoriaPares.objects.create(
                        tutoria = tutoria,
                        nombre_pares = alumnos_asesores[i],
                        boleta_pares = boletas_asesores[i],
                        unidad_pares = unidades_asesores[i]
                    )
                    tuto_pares.save()
#-------------------------------------------------------------------------------------------
#-------GUARDAR TUTORÍAS INDIVIDUALES ------------------------------------------------------
        if tutorias_registradas[2]=="ocultar":
            tutoria = Tutorias.objects.create(
                tipo = "Individual",
                profesor = profesor_form
            )
            tuto_individual = TutoriaIndividual.objects.create(
                tutoria = tutoria,
                no_hombres_individual = request.POST.get("numero_hombres_individual"),
                no_mujeres_individual = request.POST.get("numero_mujeres_individual"),
                lista_alumnos_individual = request.POST.get("lista_alumnos_individual")
            )
            tuto_individual.save()
#-------------------------------------------------------------------------------------------
#------ GUARDAR TUTORÍAS DE MOVILIDAD ------------------------------------------------------
        if tutorias_registradas[3]=="ocultar":
            alumnos_movilidad = request.POST.get("nombre_alumnos_movilidad")
            print(alumnos_movilidad)
            
            lista_alumnos = listar_alumnos(alumnos_movilidad)
            print(lista_alumnos)
            if falta_datos(lista_alumnos):
                eliminar_profesor(request,profesor_form.id)
                messages.error(request, "Faltaron campos por llenar. Revisa los campos en la sección: Tutoria entre pares.")
                return render(request,"formulario.html",{"tipo":"falta_datos"})
            
            tutoria = Tutorias.objects.create(
                tipo = "Movilidad",
                profesor = profesor_form
            )
            tuto_movilidad = TutoriaMovilidad.objects.create(
                tutoria = tutoria,
                boleta_nombre = alumnos_movilidad,
                no_hombres_movilidad = request.POST.get("numero_hombres_movilidad"),
                no_mujeres_movilidad = request.POST.get("numero_mujeres_movilidad"),
            )
            tuto_movilidad.save()
#-------------------------------------------------------------------------------------------
#------ GUARDAR TUTORÍAS DE REGULARIZACIÓN -------------------------------------------------
        if tutorias_registradas[4]=="ocultar":
            tutoria = Tutorias.objects.create(
                tipo = "Regularización",
                profesor = profesor_form
            )
            tuto_regularizacion = TutoriaRegularizacion.objects.create(
                tutoria = tutoria,
                unidad_aprendizaje_regularizacion = request.POST.get("unidad_regularizacion"),
                carrera_regularizacion = request.POST.get("carrera_regularizacion"),
                no_hombres_regularizacion = request.POST.get("numero_hombres_regularizacion"),
                no_mujeres_regularizacion = request.POST.get("numero_mujeres_regularizacion"),
                lista_alumnos_regularizacion = request.POST.get("lista_alumnos_regularizacion")
            )
            tuto_regularizacion.save()
#-------------------------------------------------------------------------------------------
#------ GUARDAR TUTORÍAS DE RECUPERACIÓN ---------------------------------------------------
        if tutorias_registradas[5]=="ocultar":
            tutoria = Tutorias.objects.create(
                tipo = "Recuperación",
                profesor = profesor_form
            )
            tuto_recuperacion = TutoriaRecuperacion.objects.create(
                tutoria = tutoria,
                unidad_aprendizaje_recuperacion = request.POST.get("unidad_recuperacion"),
                carrera_recuperacion = request.POST.get("carrera_recuperacion"),
                no_hombres_recuperacion = request.POST.get("numero_hombres_recuperacion"),
                no_mujeres_recuperacion = request.POST.get("numero_mujeres_recuperacion"),
                lista_alumnos_recuperacion = request.POST.get("lista_alumnos_recuperacion")
            )
            tuto_recuperacion.save()
        return render(request,"responseHTML/success.html",{"tipo":"registro"})
    except Exception as e:
        eliminar_profesor(request,profesor_form.id)
        return render(request,"formulario.html",{
			'error': e,
		})    

#ELIMINAR REGISTRO DEL PROFESOR Y SUS TUTORÍAS -------------  ----------------------------------
def eliminar_profesor(request,profesor_id):
    try:
        profesor = get_object_or_404(Profesor, id=profesor_id)
        profesor.delete()
    except:
        return render(request,"responseHTML/failure.html")

#INICIAR SESIÓN --------------------------------------------------------------------------------
def signin(request):
	if request.method == "GET":
		return render(request, "signin.html",{
			'form': AuthenticationForm,
			'usuario': request.user.first_name if request.user.is_authenticated else "Invitado" 
		})
	try:
		username=request.POST['username']
		password=request.POST['password']
		user = User.objects.get(username=username)
		if not user.is_active:
			return render(request, "signin.html", { "error": "Tu cuenta está inactiva. Contacta al administrador." })
		auth = authenticate(request,username=username,password=password)
		if auth is None:
			return render(request, "signin.html",{
				'form': AuthenticationForm,
				'error': "Credenciales incorrectas. Intenta nuevamente"
			})
		else:
			login(request,auth)
			return redirect("administrador")
	except User.DoesNotExist:
		return render(request, "signin.html", { "error": "Usuario no registrado." })

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
