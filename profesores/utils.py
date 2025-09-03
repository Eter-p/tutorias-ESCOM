from django.core.mail import send_mail

from .models import Profesor
from tutorias.utils import periodo_actual
from tutorias.models import TutoriaGrupal,TutoriaIndividual,TutoriaMovilidad,TutoriaPares,TutoriaRecuperacion,TutoriaRegularizacion
from pprint import pprint
# FLITAR PROFESOR
def profesores_ha_registrado(periodo_selecionado):
    """ Se filtarán y descartaran los profesores que no hayan hecho ningun registro en el perido actual"""
    lista_profesores = Profesor.objects.all()
    for profesor in Profesor.objects.all():
        conteo_tutorias = 0

        conteo_tutorias += len(TutoriaGrupal.objects.filter(tutoria__profesor=profesor,tutoria__periodo__nombre_periodo=periodo_selecionado))
        conteo_tutorias += len(TutoriaIndividual.objects.filter(tutoria__profesor=profesor,tutoria__periodo__nombre_periodo=periodo_selecionado))
        conteo_tutorias += len(TutoriaPares.objects.filter(tutoria__profesor=profesor,tutoria__periodo__nombre_periodo=periodo_selecionado))
        conteo_tutorias += len(TutoriaRecuperacion.objects.filter(tutoria__profesor=profesor,tutoria__periodo__nombre_periodo=periodo_selecionado))
        conteo_tutorias += len(TutoriaRegularizacion.objects.filter(tutoria__profesor=profesor,tutoria__periodo__nombre_periodo=periodo_selecionado))
        conteo_tutorias += len(TutoriaMovilidad.objects.filter(tutoria__profesor=profesor,tutoria__periodo__nombre_periodo=periodo_selecionado))
        if conteo_tutorias == 0:
            lista_profesores = lista_profesores.exclude(id=profesor.id)
    return lista_profesores.order_by("nombre")

def asignar_grupos(tutorias_grupales):
    """ Obtener el registro de tutorias ordenado pero sin las fechas """
    tutorias_ordenadas = []
    for tutoria,grupos in tutorias_grupales.items():
        registro_profesor = []
        registro_profesor.append(tutoria[1])
        for grupo in grupos:
            registro_profesor.append(grupo)
        tutorias_ordenadas.append(registro_profesor)
    return asignar_grupo(tutorias_ordenadas,obtener_profesores(tutorias_ordenadas),obtener_grupos(tutorias_ordenadas),1,[])

def obtener_grupos(tabla_filtrada):
    lista_grupos = []
    for registro in tabla_filtrada:
        for grupo in registro[1:]:
            if grupo != "X":
                if not grupo in lista_grupos:
                    lista_grupos.append(grupo)
    return sorted(lista_grupos)

def obtener_profesores(tabla_flitrada):
    lista_profesores = []
    for registro in tabla_flitrada:
        lista_profesores.append(registro[0])
    return lista_profesores

def buscar_profesor(nombre,tabla):
    for i,fila in enumerate(tabla):
        if nombre == fila[0]:
            return i
      
def buscar_grupo(grupo,tabla,columna):
    for i,fila in enumerate(tabla):
        if grupo == fila[columna]:
            return i
        
def asignar_grupo(base_datos,lista_profesores,lista_grupos,intento,tabla_asignada):
    if not lista_profesores:
        return tabla_asignada
    indice = buscar_profesor(lista_profesores[0],base_datos)
    profesor_grupo = []
    if intento<=3:
        if base_datos[indice][intento] in lista_grupos:
            profesor_grupo.append(lista_profesores.pop(0))
            lista_grupos.remove(base_datos[indice][intento])
            profesor_grupo.append(base_datos[indice][intento])
            tabla_asignada.append(profesor_grupo)
            intento = 1
            return asignar_grupo(base_datos,lista_profesores,lista_grupos,intento,tabla_asignada)
        else:
            return asignar_grupo(base_datos,lista_profesores,lista_grupos,intento+1,tabla_asignada)
    if intento>3:
        intento = next((i for i, x in enumerate(base_datos[indice][1:], start=1) if x is not None), None)
        indice_asignada = buscar_grupo(base_datos[indice][intento],tabla_asignada,1)
        lista_profesores.insert(1,tabla_asignada[indice_asignada][0])
        lista_grupos.append(tabla_asignada[indice_asignada][1])
        n_indice = buscar_profesor(tabla_asignada[indice_asignada][0],base_datos)
        base_datos[n_indice][base_datos[n_indice].index(tabla_asignada[indice_asignada][1])] = None
        tabla_asignada.remove(tabla_asignada[indice_asignada])
        return asignar_grupo(base_datos,lista_profesores,lista_grupos,intento,tabla_asignada)

# ENVIA CORREOS ELECTRONICOS
def enviar_correo(uid,token,user):
    activation_link = f"http://localhost:8000/activate/{uid}/{token}/"
    send_mail(
        subject="Activa tu cuenta",
        message=f"Se hizo un registro del usuario {user.username} en el Sistema de Tutorías de la ESCOM. Activa tu cuenta usando este enlace: {activation_link}. Si usted no reconoce esta actividad, ignore este correo.",
        from_email="smpmo.p@gmail.com",
        recipient_list=[user.email],
    )