from django import forms
from .models import Valoracion

class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ["puntuacion", "comentario", "fecha_valoracion"]