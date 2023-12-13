from datetime import date, timedelta
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from .models import Libro, Prestamos
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

class ListadoBook(ListView):
    model = Libro
    template_name = 'bibliotecaapp/listado_libro.html'
    queryset = Libro.objects.filter(disponibilidad="disponible")
    
class ListadoPrestado(ListView):
    model = Prestamos
    template_name = 'bibliotecaapp/libros_prestados.html'
    #queryset = Prestamos.objects.filter(estado='prestado')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
    
        context['prestamo_prestados'] = Prestamos.objects.filter(estado='prestado', usuario=self.request.user)
        context['prestamo_devuelto'] = Prestamos.objects.filter(estado='devuelto', usuario=self.request.user)
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

class Realizar_Prestamo(View):
    realizarPrestamos_template = 'bibliotecaapp/prestamo_libro.html'
    def get(self,request, pk):
        libroPrestado = get_object_or_404(Libro, pk=pk)
        return render(request, self.realizarPrestamos_template, {'libro': libroPrestado})
    
    def post(self, request, pk):
        libroPrestado = get_object_or_404(Libro, pk=pk)
        if request.method == 'POST':
            usuario = request.user
            fechaPrestamo = date.today()
            fechaDevolucion = fechaPrestamo + timedelta(days=15)
            
            Prestamos.objects.create(
                libro = libroPrestado,
                fecha_prestamo = fechaPrestamo,
                fecha_devolucion = fechaDevolucion,
                usuario = usuario,
                estado = 'prestado'
            )
            libroPrestado.disponibilidad = "prestado"
            libroPrestado.save()
            return redirect('details', pk = pk)
        return render(request, self.realizarPrestamos_template, {'libro' : libroPrestado})

class Devolver_Prestamo(View):
    devolverPrestamo_template = 'bibliotecaapp/devolver_libro.html'
    
    def get(self, request, pk):
        libroDevuelto = get_object_or_404(Libro, pk=pk, disponibilidad = 'prestado')
        return render(request, self.devolverPrestamo_template, {'libro': libroDevuelto})
    
    def post(self, request, pk):
        libroDevuelto = get_object_or_404(Libro, pk=pk, disponibilidad = 'prestado')
        prestamo = Prestamos.objects.filter(libro = libroDevuelto, usuario = request.user, estado = 'prestado').first()
        if request.method == 'POST':
            prestamo.estado = 'devuelto'
            prestamo.fecha_devolucion = date.today()
            prestamo.save()

            libroDevuelto.disponibilidad = 'disponible'
            libroDevuelto.save()
            return redirect('details', pk = pk)
        return render(request, self.devolverPrestamo_template, {'libro' : libroDevuelto})
