from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Libro
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

class ListadoBook(ListView):
    model = Libro
    template_name = 'bibliotecaapp/listado.html'

class DetailsBook(DetailView):
    model = Libro
    template_name = 'bibliotecaapp/details.html'

class EditBook(UpdateView):
    model = Libro
    fields = ["titulo", "autores", "editorial", "fecha_publicacion", "genero", "isbn", "resumen", "disponibilidad", "portada"]
    template_name = 'bibliotecaapp/update.html'
    success_url = reverse_lazy('listado')

class DeleteBook(DeleteView):
    model = Libro
    template_name = 'bibliotecaapp/delete.html'
    success_url = reverse_lazy('listado')

class CreateBook(CreateView):
    model = Libro
    fields = ["titulo", "autores", "editorial", "fecha_publicacion", "genero", "isbn", "resumen", "disponibilidad", "portada"]
    template_name = 'bibliotecaapp/form.html'
    success_url = reverse_lazy('listado')