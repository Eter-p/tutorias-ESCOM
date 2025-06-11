from django.utils.timezone import now
from .models import Periodo

def periodo_actual():
    periodo_actual = None
    for periodo in Periodo.objects.all():
        if now() < periodo.fecha_cierre:
            periodo_actual = periodo
    return periodo_actual

# Para cada conjunto de datos (columna) se verifica:
# Si todos los datos estan completos, regresa False (no faltan datos)
# Si todos los datos estan vacios, regresa False (se ignora el caso)
# Si hay algunos campos vacios y otros no, regresa True (faltan datos)

def falta_datos(tabla_datos):
    for i in range(len(tabla_datos[0])):
        exiten_datos = []
        for columna in tabla_datos:
            exiten_datos.append(bool(columna[i]))
        if len(set(exiten_datos))!=1:
            return True
    return False

def listar_alumnos(alumnos_boletas):
    alumnos_boletas = alumnos_boletas.split(";")
    print(alumnos_boletas)
    lista_alumnos = []
    alumnos = []
    boletas = []
    for alumno_boleta in alumnos_boletas:
        if alumno_boleta:
            a_b = alumno_boleta.split(",")
            print(a_b)
            alumnos.append(a_b[0].strip())
            if len(a_b) < 2:
                boletas.append("")
                continue
            boletas.append(a_b[1].strip()),
    lista_alumnos.append(alumnos)
    lista_alumnos.append(boletas)
    return lista_alumnos