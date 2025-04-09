from django import forms
from .models import Profesor

class FormProfesor(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = [
            "profesor",
            "correo",
            "correo_institucional"
        ]
        labels = {
            "profesor" : "Nombre",
            "correo" : "Correo electronico",
            "correo_institucional" : "Correo instucional"
        }