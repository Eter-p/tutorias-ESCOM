from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from openpyxl import load_workbook

from profesores.utils import profesores_ha_registrado
from .models import Periodo,Tutorias,TutoriaGrupal,TutoriaPares,TutoriaIndividual,TutoriaMovilidad,TutoriaRegularizacion,TutoriaRecuperacion,ReporteExcel
from .utils import falta_datos, listar_alumnos,periodo_actual
from pprint import pprint

import ast
#REGISTRO DE LAS TUTORÍAS ------------------------------------------------------------------
@login_required
def registrar_tutoria(request,tipo):
    if request.method== "GET":
        """ Primero se verifica que tipo de tutoria se esta registrando y cuantas ya se han registrado """
        total_tutorias = 0
        if tipo == "grupal":
            total_tutorias = len(TutoriaGrupal.objects.filter(tutoria__profesor=request.user,tutoria__periodo__nombre_periodo=periodo_actual))
        if tipo == "pares":
            total_tutorias = len(TutoriaPares.objects.filter(tutoria__profesor=request.user,tutoria__periodo__nombre_periodo=periodo_actual))
        if tipo == "individual":
            total_tutorias = len(TutoriaIndividual.objects.filter(tutoria__profesor=request.user,tutoria__periodo__nombre_periodo=periodo_actual))
        if tipo == "movilidad":
            total_tutorias = len(TutoriaMovilidad.objects.filter(tutoria__profesor=request.user,tutoria__periodo__nombre_periodo=periodo_actual))
        if tipo == "regularizacion":
            total_tutorias = len(TutoriaRegularizacion.objects.filter(tutoria__profesor=request.user,tutoria__periodo__nombre_periodo=periodo_actual))
        if tipo == "recuperacion":
            total_tutorias = len(TutoriaRecuperacion.objects.filter(tutoria__profesor=request.user,tutoria__periodo__nombre_periodo=periodo_actual))
        return render(request,f"formsTutorias/{tipo}.html",{"total_tutorias":total_tutorias})
    try:
        
#-------------------------------------------------------------------------------------------
#------ GUARDAR TUTORÍAS GRUPALES ----------------------------------------------------------
        if tipo == "grupal":
            """ Recopilación de los datos del formulario de tutorías grupales """
            grupos = request.POST.getlist("grupo")
            unidades = request.POST.getlist("unidad")
            carreras = request.POST.getlist("carrera")
            hombres = request.POST.getlist("numero_hombres_grupal")
            mujeres = request.POST.getlist("numero_mujeres_grupal")
            archivos = request.POST.getlist("lista_alumnos_grupal")
            
            """ Comprueba si las datos del formulario estan completos """
            if falta_datos([grupos,unidades,hombres,mujeres,archivos]):
                messages.error(request, "Se detecto alguna falta de datos. Favor de revisar")
                return render(request,f"formsTutorias/{tipo}.html",{"tipo":"falta_datos"})
            
            """ Por cada grupo registrado en el formulario de tutorías
            grupales (maximo 3) se creará una instancia de Tutoria y una de TutoriaGrupal """
            grupos_registrados = []
            for i in [0,1,2]:
                if grupos[i]:
                    tutoria_valida = []
                    tutoria = Tutorias(
                        tipo = "Grupal",
                        profesor = request.user,
                        periodo = periodo_actual()
                    )
                    tuto_grupal = TutoriaGrupal(
                        tutoria = tutoria,
                        grupo = grupos[i],
                        unidad_aprendizaje = unidades[i],
                        carrera = carreras[i],
                        no_hombres_grupal = hombres[i],
                        no_mujeres_grupal = mujeres[i],
                        lista_alumnos_grupal = archivos[i],
                    )
                    tutoria_valida.extend([tutoria,tuto_grupal])
                    grupos_registrados.append(tutoria_valida)
            
            """ Si no ocurrio ningún problema se guardará en la base de datos cada instancia creada """
            for grupo in grupos_registrados:
                grupo[0].save()
                grupo[1].save()
#-------------------------------------------------------------------------------------------
#------ GUARDAR TUTORÍAS ENTRE PARES -------------------------------------------------------
        if tipo == "pares":
            """ Recopilación de los datos del formulario de tutorías entre pares """
            alumnos_asesores = request.POST.getlist("nombre_alumno_asesor")
            boletas_asesores = request.POST.getlist("boleta_alumno_asesor")
            unidades_asesores = request.POST.getlist("unidad_aprendizaje_pares")
            
            """ Comprueba si las datos del formulario estan completos """
            if falta_datos([alumnos_asesores,boletas_asesores,unidades_asesores]):
                messages.error(request, "Se detecto alguna falta de datos. Favor de revisar")
                return render(request,f"formsTutorias/{tipo}.html",{"tipo":"falta_datos"})
            
            """ Por cada alumno asesor registrado en el formulario de tutorías
            entre pares (maximo 2) se creará una instancia de Tutoria y una de TutoriaPares """
            alumnos_registrados = []
            for i in [0,1]:
                if alumnos_asesores[i]:
                    alumno_valido = []
                    tutoria = Tutorias(
                        tipo = "Pares",
                        profesor = request.user,
                        periodo = periodo_actual()
                    )
                    tuto_pares = TutoriaPares(
                        tutoria = tutoria,
                        nombre_pares = alumnos_asesores[i],
                        boleta_pares = boletas_asesores[i],
                        unidad_pares = unidades_asesores[i]
                    )
                    alumno_valido.extend([tutoria,tuto_pares])
                    alumnos_registrados.append(alumno_valido)
            
            """ Si no ocurrio ningún problema se guardará en la base de datos cada instancia creada """
            for alumno in alumnos_registrados:
                alumno[0].save()
                alumno[1].save()
#-------------------------------------------------------------------------------------------
#-------GUARDAR TUTORÍAS INDIVIDUALES ------------------------------------------------------
        if tipo == "individual":
            """ Se crearán unicamente una instacia de Tutoria y una de TutoriaIndivudual por cada profesor"""
            tutoria = Tutorias(
                tipo = "Individual",
                profesor = request.user,
                periodo = periodo_actual()
            )
            tuto_individual = TutoriaIndividual(
                tutoria = tutoria,
                no_hombres_individual = request.POST.get("numero_hombres_individual"),
                no_mujeres_individual = request.POST.get("numero_mujeres_individual"),
                lista_alumnos_individual = request.POST.get("lista_alumnos_individual")
            )
            tutoria.save()
            tuto_individual.save()
#-------------------------------------------------------------------------------------------
#------ GUARDAR TUTORÍAS DE MOVILIDAD ------------------------------------------------------
        if tipo == "movilidad":
            """ Recopilación de los datos de los alumnos del formulario de Tutorías de movilidad """
            alumnos_movilidad = request.POST.get("nombre_alumnos_movilidad")

            """ Transformación de los datos del alumno a una lista boleta-alumno """
            lista_alumnos = listar_alumnos(alumnos_movilidad)
            
            """ Comprueba que los datos del alumno esten completos """
            if falta_datos(lista_alumnos):
                messages.error(request, "Se detecto alguna falta de datos. Favor de revisar")
                return render(request,f"formsTutorias/{tipo}.html",{"tipo":"falta_datos"})
            
            """ Si bien se genero una lista de alumnos se crearán unicamente una instancia de Tutoria
            y una de TutoríaMovilidad """
            tutoria = Tutorias(
                tipo = "Movilidad",
                profesor = request.user,
                periodo = periodo_actual()
            )
            tuto_movilidad = TutoriaMovilidad(
                tutoria = tutoria,
                boleta_nombre = alumnos_movilidad,
                no_hombres_movilidad = request.POST.get("numero_hombres_movilidad"),
                no_mujeres_movilidad = request.POST.get("numero_mujeres_movilidad"),
            )
            tutoria.save()
            tuto_movilidad.save()
#-------------------------------------------------------------------------------------------
#------ GUARDAR TUTORÍAS DE REGULARIZACIÓN -------------------------------------------------
        """ Se crearán unicamente una instacia de Tutoria y una de TutoriaRegularizacion por cada profesor"""
        if tipo == "regularizacion":
            tutoria = Tutorias(
                tipo = "Regularización",
                profesor = request.user,
                periodo = periodo_actual()
            )
            tuto_regularizacion = TutoriaRegularizacion(
                tutoria = tutoria,
                unidad_aprendizaje_regularizacion = request.POST.get("unidad_regularizacion"),
                carrera_regularizacion = request.POST.get("carrera_regularizacion"),
                no_hombres_regularizacion = request.POST.get("numero_hombres_regularizacion"),
                no_mujeres_regularizacion = request.POST.get("numero_mujeres_regularizacion"),
                lista_alumnos_regularizacion = request.POST.get("lista_alumnos_regularizacion")
            )
            tutoria.save()
            tuto_regularizacion.save()
#-------------------------------------------------------------------------------------------
#------ GUARDAR TUTORÍAS DE RECUPERACIÓN ---------------------------------------------------
        if tipo == "recuperacion":
            """ Se crearán unicamente una instacia de Tutoria y una de TutoriaRecuperación por cada profesor"""
            tutoria = Tutorias.objects.create(
                tipo = "Recuperación",
                profesor = request.user,
                periodo = periodo_actual()
            )
            tuto_recuperacion = TutoriaRecuperacion.objects.create(
                tutoria = tutoria,
                unidad_aprendizaje_recuperacion = request.POST.get("unidad_recuperacion"),
                carrera_recuperacion = request.POST.get("carrera_recuperacion"),
                no_hombres_recuperacion = request.POST.get("numero_hombres_recuperacion"),
                no_mujeres_recuperacion = request.POST.get("numero_mujeres_recuperacion"),
                lista_alumnos_recuperacion = request.POST.get("lista_alumnos_recuperacion")
            )
            tutoria.save()
            tuto_recuperacion.save()
        return render(request,"responseHTML/success.html",{"success":"tutoria registrada"})
    except Exception as e:
        return render(request,"responseHTML/failure.html",{"failure":"tutoria", "error":e})

def eliminar_tutoria(request,id_tutoria):
    try:
        tutoria = Tutorias.objects.get(id=id_tutoria)
        tutoria.delete()
    except:
        return render(request,"responseHTML/failure.html")

@login_required
def listar_tutorias_admin(request,tipo,periodo):
    if tipo == "grupales":
        tipo_tutoria = TutoriaGrupal
        template = "viewsTutorias/grupales.html"
    elif tipo == "pares":
        tipo_tutoria = TutoriaPares
        template = "viewsTutorias/pares.html"
    elif tipo == "individuales":
        tipo_tutoria = TutoriaIndividual
        template = "viewsTutorias/individuales.html"
    elif tipo == "movilidad":
        tipo_tutoria = TutoriaMovilidad
        template = "viewsTutorias/movilidad.html"
    elif tipo == "recuperacion":
        tipo_tutoria = TutoriaRecuperacion
        template = "viewsTutorias/recuperacion.html"
    elif tipo == "regularizacion":
        tipo_tutoria = TutoriaRegularizacion
        template = "viewsTutorias/regularizacion.html"

    profesores = profesores_ha_registrado(periodo)

    query = request.GET.get("q", "")
    resultados = profesores.filter(nombre__icontains=query) if query else profesores
    tutorias_filtradas = flitrar_datos(request,tipo_tutoria,periodo)

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
        "periodo":periodo
	})

@login_required
def listar_tutorias_user(request,tipo):
    if tipo == "grupales":
        tipo_tutoria = TutoriaGrupal
        template = "viewsTutorias/grupales.html"
    elif tipo == "pares":
        tipo_tutoria = TutoriaPares
        template = "viewsTutorias/pares.html"
    elif tipo == "individuales":
        tipo_tutoria = TutoriaIndividual
        template = "viewsTutorias/individuales.html"
    elif tipo == "movilidad":
        tipo_tutoria = TutoriaMovilidad
        template = "viewsTutorias/movilidad.html"
        
    elif tipo == "recuperacion":
        tipo_tutoria = TutoriaRecuperacion
        template = "viewsTutorias/recuperacion.html"
    elif tipo == "regularizacion":
        tipo_tutoria = TutoriaRegularizacion
        template = "viewsTutorias/regularizacion.html"

    lista_tutorias = tipo_tutoria.objects.filter(tutoria__profesor = request.user, tutoria__periodo=periodo_actual())
    boletas_alumnos = {}
    if tipo_tutoria == TutoriaMovilidad:
        for instancia in lista_tutorias:
            boletas_alumnos = {}
            for boleta_alumno in instancia.boleta_nombre.split(";"):
                boleta,alumno = boleta_alumno.split(",")
                boletas_alumnos[boleta] = alumno
                
    return render(request,template,{"lista_tutorias": lista_tutorias, "alumnos": boletas_alumnos})

@login_required
def flitrar_datos(request,tipo_tutoria,periodo):
    tutorias_filtradas = tipo_tutoria.objects.select_related('tutoria__profesor').filter(tutoria__periodo__nombre_periodo=periodo)
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
    return tutorias_filtradas.order_by("tutoria__profesor__nombre")

@login_required
def upload_excel(request,periodo):
    data = []
    if request.method == 'POST' and request.FILES.get('archivo'):
        excel_file = request.FILES['archivo']
        wb = load_workbook(excel_file, data_only=True)
        ws = wb.active
        i = 0
        requisitos = {"carrera":False,"genero":False,"reprobadas":False,"desfasadas":False}

        for row in ws.iter_rows(values_only=True):
            for item in row:
                for subtexto in requisitos.keys():
                    encontrado = subtexto in str(item).lower()
                    if encontrado:
                        requisitos[subtexto] = encontrado
                        continue
            if i==2:
                break
            i=i+1
        for row in ws.iter_rows(values_only=True):
            data.append(row)
        return render(request, 'get_reporte_excel.html', {'data': data,'periodo':periodo,'requisitos':requisitos})
    reporte = ReporteExcel.objects.filter(periodo__nombre_periodo=periodo)
    if reporte:
        data = {}
        for tabla in reporte:
            sumas = {
                "hombres" : tabla.hombres_regular + tabla.hombres_irregular,
                "mujeres" : tabla.mujeres_regular + tabla.mujeres_irregular,
                "regulares" : tabla.hombres_regular + tabla.mujeres_regular,
                "irregulares" : tabla.hombres_irregular + tabla.mujeres_irregular,
                "total" : tabla.hombres_regular + tabla.hombres_irregular + tabla.mujeres_regular + tabla.mujeres_irregular
            }
            data[tabla] = sumas
        return render(request, 'reporte_excel.html', {'data': data,'periodo':periodo})
    return render(request, 'get_reporte_excel.html', {'data': data,'periodo':periodo})

@login_required
def generar_reporte_excel(request,periodo):
    if request.method == 'GET':
        return redirect("reporte_exel")
    try:
        confirmacion = ast.literal_eval(request.POST.get("confirmacion"))
        contadores = {}
        if not confirmacion:
            data_recibida = ast.literal_eval(request.POST.get("informacion"))
            error_data = []
            columna = {"carrera":0,"genero":0,"reprobadas":0,"desfasadas":0}
            contadores = {
                "isc_hombres_regular": 0,
                "isc_mujeres_regular": 0,
                "isc_hombres_irregular": 0,
                "isc_mujeres_irregular": 0,
                "iia_hombres_regular": 0,
                "iia_mujeres_regular": 0,
                "iia_hombres_irregular": 0,
                "iia_mujeres_irregular": 0,
                "lcd_hombres_regular": 0,
                "lcd_mujeres_regular": 0,
                "lcd_hombres_irregular": 0,
                "lcd_mujeres_irregular": 0,
                "isisa_hombres_regular": 0,
                "isisa_mujeres_regular": 0,
                "isisa_hombres_irregular": 0,
                "isisa_mujeres_irregular": 0
            }
            
            for i,col in enumerate(data_recibida.pop(0)):
                if  col.lower() == "carrera":
                    columna["carrera"] = i
                if  col.lower() == "genero":
                    columna["genero"] = i
                if  col.lower() == "reprobadas":
                    columna["reprobadas"] = i
                if  col.lower() == "desfasadas":
                    columna["desfasadas"] = i

            for i,linea in enumerate(data_recibida):
                if linea[columna["carrera"]] == "ING. EN SIS. COMPUTACIONALES":
                    if linea[columna["genero"]] == "HOMBRE":
                        if (int(linea[columna["reprobadas"]])+int(linea[columna["desfasadas"]]))==0:
                            contadores["isc_hombres_regular"] += 1
                        else:
                            contadores["isc_hombres_irregular"] += 1
                    elif linea[columna["genero"]] == "MUJER":
                        if (int(linea[columna["reprobadas"]])+int(linea[columna["desfasadas"]]))==0:
                            contadores["isc_mujeres_regular"] += 1
                        else:
                            contadores["isc_mujeres_irregular"] += 1
                    else:
                        error_data.append(i+2)
                elif linea[columna["carrera"]] == "INGENIERIA EN INTELIGENCIA ARTIFICIAL":
                    if linea[columna["genero"]] == "HOMBRE":
                        if (int(linea[columna["reprobadas"]])+int(linea[columna["desfasadas"]]))==0:
                            contadores["iia_hombres_regular"] +=  1
                        else:
                            contadores["iia_hombres_irregular"] += 1
                    elif linea[columna["genero"]] == "MUJER":
                        if (int(linea[columna["reprobadas"]])+int(linea[columna["desfasadas"]]))==0:
                            contadores["iia_mujeres_regular"] += 1
                        else:
                            contadores["iia_mujeres_irregular"] += 1
                    else:
                        error_data.append(i+2)
                elif linea[columna["carrera"]] == "LICENCIATURA EN CIENCIA DE DATOS":
                    if linea[columna["genero"]] == "HOMBRE":
                        if (int(linea[columna["reprobadas"]])+int(linea[columna["desfasadas"]]))==0:
                            contadores["lcd_hombres_regular"] += 1
                        else:
                            contadores["lcd_hombres_irregular"] +=  1
                    elif linea[columna["genero"]] == "MUJER":
                        if (int(linea[columna["reprobadas"]])+int(linea[columna["desfasadas"]]))==0:
                            contadores["lcd_mujeres_regular"] += 1
                        else:
                            contadores["lcd_mujeres_irregular"] += 1
                    else:
                        error_data.append(i+2)
                elif linea[columna["carrera"]] == "ING. EN SISTEMAS AUTOMOTRICES":
                    if linea[columna["genero"]] == "HOMBRE":
                        if (int(linea[columna["reprobadas"]])+int(linea[columna["desfasadas"]]))==0:
                            contadores["isisa_hombres_regular"] += 1
                        else:
                            contadores["isisa_hombres_irregular"] += 1
                    elif linea[columna["genero"]] == "MUJER":
                        if (int(linea[columna["reprobadas"]])+int(linea[columna["desfasadas"]]))==0:
                            contadores["isisa_mujeres_regular"] += 1
                        else:
                            contadores["isisa_mujeres_irregular"] += 1
                    else:
                        error_data.append(i+2)
                else:
                    error_data.append(i+2)
            if len(error_data) > 0:
                return render(request,"responseHTML/failure.html", {"failure":"error_reporte","data":contadores,"error_data":error_data,"periodo":periodo})
        if confirmacion:
            contadores = ast.literal_eval(request.POST.get("informacion"))
            
        periodo_id = Periodo.objects.get(nombre_periodo = periodo)
        r_isc = ReporteExcel(
            periodo = periodo_id,
            carrera = "isc",
            hombres_regular = contadores["isc_hombres_regular"],
            mujeres_regular = contadores["isc_hombres_irregular"],
            hombres_irregular = contadores["isc_mujeres_regular"],
            mujeres_irregular = contadores["isc_mujeres_irregular"],
        )
        r_iia = ReporteExcel(
            periodo = periodo_id,
            carrera = "iia",
            hombres_regular = contadores["iia_hombres_regular"],
            mujeres_regular = contadores["iia_hombres_irregular"],
            hombres_irregular = contadores["iia_mujeres_regular"],
            mujeres_irregular = contadores["iia_mujeres_irregular"],
        )
        r_lcd = ReporteExcel(
            periodo = periodo_id,
            carrera = "lcd",
            hombres_regular = contadores["lcd_hombres_regular"],
            mujeres_regular = contadores["lcd_hombres_irregular"],
            hombres_irregular = contadores["lcd_mujeres_regular"],
            mujeres_irregular = contadores["lcd_mujeres_irregular"],
        )
        r_isisa = ReporteExcel(
            periodo = periodo_id,
            carrera = "isisa",
            hombres_regular = contadores["isisa_hombres_regular"],
            mujeres_regular = contadores["isisa_hombres_irregular"],
            hombres_irregular = contadores["isisa_mujeres_regular"],
            mujeres_irregular = contadores["isisa_mujeres_irregular"],
        )
        r_escom = ReporteExcel(
            periodo = periodo_id,
            carrera = "ESCOM",
            hombres_regular = contadores["isc_hombres_regular"] + contadores["iia_hombres_regular"] + contadores["lcd_hombres_regular"] + contadores["isisa_hombres_regular"],
            mujeres_regular = contadores["isc_mujeres_regular"] + contadores["iia_mujeres_regular"] + contadores["lcd_mujeres_regular"] + contadores["isisa_mujeres_regular"],
            hombres_irregular = contadores["isc_hombres_irregular"] + contadores["iia_hombres_irregular"] + contadores["lcd_hombres_irregular"] + contadores["isisa_hombres_irregular"],
            mujeres_irregular = contadores["isc_mujeres_irregular"] + contadores["iia_mujeres_irregular"] + contadores["lcd_mujeres_irregular"] + contadores["isisa_mujeres_irregular"]
        )
        r_isc.save()
        r_iia.save()
        r_lcd.save()
        r_isisa.save()
        r_escom.save()
        return redirect("reporte_excel",periodo)
    except Exception as e:
        return render(request,"responseHTML/failure.html",{"error":e})

@login_required
def  eliminar_reporte(request,periodo):
    try:
        ReporteExcel.objects.filter(periodo__nombre_periodo=periodo).delete()
        return redirect ("reporte_excel",periodo)
    except Exception as e:
        return render(request,"responseHTML/failure.html",{"error":e})