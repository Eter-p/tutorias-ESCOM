from django import forms
from .models import Periodo,Tutorias,TutoriaGrupal,TutoriaPares,TutoriaIndividual,TutoriaMovilidad,TutoriaRegularizacion,TutoriaRecuperacion

class FormPerido(forms.ModelForm):
    class Meta:
        model = Periodo
        fields =[
            "nombre_periodo",
            "fecha_apertura",
            "fecha_cierre"
        ]
        labels = {
            "nombre_periodo": "Nombre del periodo",
            "fecha_apertura": "Fecha de apertura",
            "fecha_cierre": "Fecha de cierre"
        }

class FormTutorias(forms.ModelForm):
    class Meta:
        model = Tutorias
        fields =[
            "tipo",
            "profesor",
            "periodo",
            "fecha"
        ]
        labels = {
            "fecha": "Fecha de registro",
            "tipo": "Tipo de tutoría",
            "periodo": "Periodo",
            "profesor": "Profesor"
        }

class FormTutoriaGrupal(forms.ModelForm):
    class Meta:
        model = TutoriaGrupal
        fields =[
            "tutoria",
            "grupo",
            "unidad_aprendizaje",
            "carrera",
            "no_hombres_grupal",
            "no_mujeres_grupal",
            "lista_alumnos_grupal",
            "tutoria_asignada"
        ]
        labels = {
            "tutoria": "Tutoria - ID",
            "grupo": "Grupo",
            "unidad_aprendizaje": "Unidad de aprendizaje",
            "carrera": "Carrera",
            "no_hombres_grupal": "Número de hombres",
            "no_mujeres_grupal": "Número de mujeres",
            "lista_alumnos_grupal": "Lista de alumnos",
            "tutoria_asignada": "Tutoría asignada"
        }

class FormTutoriaPares(forms.ModelForm):
    class Meta:
        model = TutoriaPares
        fields = [
            "tutoria",
            "nombre_pares",
            "boleta_pares",
            "unidad_pares"
        ]
        labels = {
            "tutoria": "Tutoria - ID",
            "nombre_pares" : "Nombre",
            "boleta_pares" : "Boleta",
            "unidad_pares" : "Unidad de aprendizaje",
        }

class FormTutoriaIndividual(forms.ModelForm):
    class Meta:
        model = TutoriaIndividual
        fields = [
            "tutoria",
            "no_hombres_individual",
            "no_mujeres_individual",
            "lista_alumnos_individual"
        ]
        labels = {
            "tutoria": "Tutoria - ID",
            "no_hombres_individual" : "Número de Hombres",
            "no_mujeres_individual" : "Número de Mujeres",
            "lista_alumnos_individual" : "Lista de alumnos"
        }

class FormTutoriaMovilidad(forms.ModelForm):
    class Meta:
        model = TutoriaMovilidad
        fields = [
            "tutoria",
            "boleta_nombre",
            "no_hombres_movilidad",
            "no_mujeres_movilidad"
        ]
        labels = {
            "tutoria": "Tutoria - ID",
            "boleta_nombre" : "Alumnos de movilidad",
            "no_hombres_movilidad" : "Número de Hombres",
            "no_mujeres_movilidad" : "Número de Mujeres"
        }

class FormTutoriaRegularizacion(forms.ModelForm):
    class Meta:
        model = TutoriaRegularizacion
        fields = [
            "tutoria",
            "unidad_aprendizaje_regularizacion",
            "carrera_regularizacion",
            "no_hombres_regularizacion",
            "no_mujeres_regularizacion",
            "lista_alumnos_regularizacion"
        ]
        labels = {
            "tutoria": "Tutoria - ID",
            "unidad_aprendizaje_regularizacion" : "Unidad de aprendizaje",
            "carrera_regularizacion" : "Carrera",
            "no_hombres_regularizacion" : "Número de Mujeres",
            "no_mujeres_regularizacion" : "Número de Mujeres",
            "lista_alumnos_regularizacion" : "Lista de alumnos"
        }

class FormTutoriaRecuperacion(forms.ModelForm):
    class Meta:
        model = TutoriaRecuperacion
        fields = [
            "tutoria",
            "unidad_aprendizaje_recuperacion",
            "carrera_recuperacion",
            "no_hombres_recuperacion",
            "no_mujeres_recuperacion",
            "lista_alumnos_recuperacion"
        ]
        labels = {
            "tutoria": "Tutoria - ID",
            "unidad_aprendizaje_recuperacion" : "Unidad de aprendizaje",
            "carrera_recuperacion" : "Carrera",
            "no_hombres_recuperacion" : "Número de Mujeres",
            "no_mujeres_recuperacion" : "Número de Mujeres",
            "lista_alumnos_recuperacion" : "Lista de alumnos"
        }
