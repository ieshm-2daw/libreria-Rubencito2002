from datetime import date, timedelta
from django.utils import timezone
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from bibliotecaapp.forms import ValoracionForm, FiltroLibroForm
from .models import *
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

class CreateBook(CreateView):
    model = Libro
    fields = ["titulo", "autores", "editorial", "fecha_publicacion", "genero", "isbn", "resumen", "portada"]
    template_name = 'bibliotecaapp/book/create_libro.html'
    success_url = reverse_lazy('listado')

class EditBook(UpdateView):
    model = Libro
    fields = ["titulo", "autores", "editorial", "fecha_publicacion", "genero", "isbn", "resumen", "portada"]
    template_name = 'bibliotecaapp/book/update_libro.html'
    success_url = reverse_lazy('listado')

class DeleteBook(DeleteView):
    model = Libro
    template_name = 'bibliotecaapp/book/delete_libro.html'
    success_url = reverse_lazy('listado')

class DetailsBook(DetailView):
    model = Libro
    template_name = 'bibliotecaapp/book/details_libro.html'

class ListadoBook(ListView):
    model = Libro
    template_name = 'bibliotecaapp/book/listado_libro.html'
    queryset = Libro.objects.filter(disponibilidad="disponible")
    paginate_by = 2
    
class ListadoPrestado(ListView):
    model = Prestamos
    template_name = 'bibliotecaapp/prestamos/libros_prestados.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
    
        context['prestamo_prestados'] = Prestamos.objects.filter(estado='prestado', usuario=self.request.user)
        context['prestamo_devuelto'] = Prestamos.objects.filter(estado='devuelto', usuario=self.request.user)
        return context

class ListadoPorFecha(ListView):
    model = Libro
    template_name = 'bibliotecaapp/book/listado_libroFecha.html'
    context_object_name = 'libros'
    ordering = ['fecha_publicacion']
    paginate_by = 2


class Realizar_Prestamo(View):
    realizarPrestamos_template = 'bibliotecaapp/prestamos/prestamo_libro.html'
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
    devolverPrestamo_template = 'bibliotecaapp/prestamos/devolver_libro.html'
    
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

# Panel de Control del bibliotecario.
class Panel_Control(ListView):
    model = Libro
    template_name = 'bibliotecaapp/panel.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # Para el total de libros prestados y disponibles.
        context['total_prestado'] = Libro.objects.filter(disponibilidad='prestado').count()
        context['total_disponible'] = Libro.objects.filter(disponibilidad='disponible').count()

        # Para los libros no devuelto.
        fecha_actual = date.today()
        context['noDevuelto'] = Prestamos.objects.filter(estado = 'prestado', fecha_devolucion__lt=fecha_actual)

        # Para los libros que expiran pronto.
        ultimaSemana = fecha_actual + timedelta(days=7)
        context['expiranPronto'] = Prestamos.objects.filter(estado = 'prestado', fecha_devolucion__lte=ultimaSemana, fecha_devolucion__gte=fecha_actual)

        return context

    def get(self, request, *args, **kwargs):
        libros = Libro.objects.all()
        lista_mas_prestado = []

        for libro in libros:
            prestamos = Prestamos.objects.filter(libro=libro)
            usuarios = []

            for prestamo in prestamos:
                if prestamo.usuario.username not in usuarios:
                    usuarios.append(prestamo.usuario.username)

            for usuario in usuarios:
                contador = 0
                for prestamo in prestamos:
                    if prestamo.usuario.username == usuario:
                        contador+=1
                if contador > 1:
                    usuarios[usuarios.index(usuario)] = usuario + ' (' + str(contador) + ')'
            lista_mas_prestado.append([libro, len(prestamos), usuarios])
        lista_mas_prestado.sort(key=lambda x: x[1], reverse=True)
        return render(request, 'bibliotecaapp/panel.html', {'lista_mas_prestado': lista_mas_prestado})

# Crear la valoracion.
class ValoracionView(CreateView):
    model = Valoracion
    fields = ["puntuacion", "comentario", "fecha_valoracion"]
    template_name = 'bibliotecaapp/valoracion/create_valoracion.html'

    def get(self, request, pk):
        form = ValoracionForm()
        usuario = self.request.user
        libro = Libro.objects.get(pk=pk)
        valoracion = Valoracion.objects.filter(libro=libro)
        return render(request, self.template_name, {'valoracion': valoracion, 'libro': libro, 'form': form, 'usuario': usuario})

    def post(self, request, pk):
        form = ValoracionForm(request.POST)
        if form.is_valid():
            libro = Libro.objects.get(pk=pk)
            valoracion = form.save(commit=False)
            valoracion.libro = libro
            valoracion.usuario = self.request.user
            valoracion.save()
            
            return redirect('listado_valoracion')
        return render(request, 'bibliotecaapp/valoracion/create_valoracion.html', { 'libro': libro,'form': form})

# Listado de Valoracion.
class ListadoValoracion(ListView):
    model = Valoracion
    template_name = 'bibliotecaapp/valoracion/listado_valoracion.html'
    ordering = ['usuario']

# Actualizar una valoracion.
class UpdateValoracion(UpdateView):
    model = Valoracion
    fields = ["puntuacion", "comentario", "fecha_valoracion"]
    template_name = 'bibliotecaapp/valoracion/update_valoracion.html'
    success_url = reverse_lazy('listado_valoracion')

# Eliminar una valoracion.
class DeleteValoracion(DeleteView):
    model = Valoracion
    template_name = 'bibliotecaapp/valoracion/delete_valoracion.html'
    success_url = reverse_lazy('listado_valoracion')

# Vista para filtrar.
class FiltroLibro(ListView):
    model = Libro
    template_name = 'bibliotecaapp/libro_list.html'
    context_object_name = 'libros'
    paginate_by = 2

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        tituloSeleccionado = self.request.GET.get('titulo')
        autoresSeleccionado = self.request.GET.get('autores')
        generoSeleccionado = self.request.GET.get('genero')
        
        if tituloSeleccionado is not None:
            queryset = queryset.filter(titulo__icontains = tituloSeleccionado)

        for autores_ID in Autor.objects.all():
            if autores_ID == autoresSeleccionado:
                queryset = queryset.filter(autores = autores_ID)

        if generoSeleccionado is not None:
            queryset = queryset.filter(genero__icontains = generoSeleccionado)

        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = FiltroLibroForm(self.request.GET)
        return context