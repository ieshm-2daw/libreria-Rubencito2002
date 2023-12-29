from django import forms
from .models import Valoracion, Libro

class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ["puntuacion", "comentario", "fecha_valoracion"]

class FiltroLibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ["titulo", "autores", "genero"]