from django import forms
from .models import Tutorias,TutoriaGrupal,TutoriaPares,TutoriaIndividual,TutoriaMovilidad,TutoriaRegularizacion

class FormTutorias(forms.ModelForm):
    class Meta:
        model = Tutorias
        fields =[
            "tipo",
            "profesor"
        ]
        labels = {
            "tipo": "Tipo de tutoría",
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
            "lista_alumnos_grupal"
        ]
        labels = {
            "tutoria": "Profesor",
            "grupo": "Grupo",
            "unidad_aprendizaje": "Unidad de aprendizaje",
            "carrera": "Carrera",
            "no_hombres_grupal": "Número de hombres",
            "no_mujeres_grupal": "Número de mujeres",
            "lista_alumnos_grupal": "Lista de alumnos"
        }

class FormTutoriaPares(forms.ModelForm):
    class Meta:
        model = TutoriaPares
        fields = [
            "tutoria",
            "nombre_pares",
            "boleta_pares"
        ]
        labels = {
            "tutoria": "Profesor",
            "nombre_pares" : "Nombres de los alumnos",
            "boleta_pares" : "Boletas de los alumnos"
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
            "tutoria": "Profesor",
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
            "tutoria": "Profesor",
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
            "tutoria": "Profesor",
            "unidad_aprendizaje_regularizacion" : "Unidad de aprendizaje",
            "carrera_regularizacion" : "Carrera",
            "no_hombres_regularizacion" : "Número de Mujeres",
            "no_mujeres_regularizacion" : "Número de Mujeres",
            "lista_alumnos_regularizacion" : "Lista de alumnos"
        }