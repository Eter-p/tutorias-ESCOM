from django import forms
from .models import Profesor

class FormProfesor(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = [
            "fecha",
            "nombre",
            "correo",
            "correo_institucional"
        ]
        labels = {
            "fecha" : "Fecha",
            "nombre" : "Nombre",
            "correo" : "Correo electronico",
            "correo_institucional" : "Correo instucional"
        }