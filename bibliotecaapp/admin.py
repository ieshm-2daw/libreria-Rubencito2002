from django.contrib import admin
from .models import Libro, Autor, Editorial, Prestamos, Usuario

admin.site.register(Libro)
admin.site.register(Autor)
admin.site.register(Editorial)
admin.site.register(Prestamos)
admin.site.register(Usuario)