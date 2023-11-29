from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Libro
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

class ListadoBook(ListView):
    model = Libro
    template_name = 'bibliotecaapp/listado_libro.html'
    #queryset = Libro.objects.filter(disponibilidad="disponible")
    """
    def get_queryset(self):
        return Libro.objects.filter(disponibilidad="disponible")
    """
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['libros_disponibles'] = Libro.objects.filter(disponibilidad="disponible")
        context['libros_prestados'] = Libro.objects.filter(disponibilidad="prestado")
        
        return context

class DetailsBook(DetailView):
    model = Libro
    template_name = 'bibliotecaapp/details_libro.html'

class EditBook(UpdateView):
    model = Libro
    fields = ["titulo", "autores", "editorial", "fecha_publicacion", "genero", "isbn", "resumen", "disponibilidad", "portada"]
    template_name = 'bibliotecaapp/update_libro.html'
    success_url = reverse_lazy('listado')

class DeleteBook(DeleteView):
    model = Libro
    template_name = 'bibliotecaapp/delete_libro.html'
    success_url = reverse_lazy('listado')

class CreateBook(CreateView):
    model = Libro
    fields = ["titulo", "autores", "editorial", "fecha_publicacion", "genero", "isbn", "resumen", "disponibilidad", "portada"]
    template_name = 'bibliotecaapp/create_libro.html'
    success_url = reverse_lazy('listado')