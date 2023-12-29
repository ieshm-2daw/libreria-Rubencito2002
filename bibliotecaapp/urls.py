from django.urls import path
from . import views
from .views import ListadoBook, ListadoPrestado, DetailsBook, EditBook, DeleteBook, CreateBook, Realizar_Prestamo, Devolver_Prestamo
from .views import ListadoPorFecha, Panel_Control, ValoracionView, ListadoValoracion, UpdateValoracion, DeleteValoracion, FiltroLibro

urlpatterns = [
    # General
    path('', ListadoBook.as_view(), name='listado'),
    
    # Libros General
    path('created/', CreateBook.as_view(), name='created'),
    path('details/<int:pk>', DetailsBook.as_view(), name='details'),
    path('edit/<int:pk>/', EditBook.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteBook.as_view(), name='delete'),
    path('listadoPrestado/', ListadoPrestado.as_view(), name='listado_prestado'),
    path('listadoFecha/', ListadoPorFecha.as_view(), name='listado_fecha'),

    # Prestamos General
    path('prestamo/<int:pk>/', Realizar_Prestamo.as_view(), name='realizar_prestamo'),
    path('devolucion/<int:pk>/', Devolver_Prestamo.as_view(), name='devolver_prestamo'),
    
    # Valoracion General
    path('valoracion/<int:pk>/', ValoracionView.as_view(), name='crear_valoracion'),
    path('editValoracion/<int:pk>/', UpdateValoracion.as_view(), name='update_valoracion'),
    path('deleteValoracion/<int:pk>/', DeleteValoracion.as_view(), name='delete_valoracion'),
    path('listadoValoracion/', ListadoValoracion.as_view(), name='listado_valoracion'),

    # Otros
    path('panel_control/', Panel_Control.as_view(), name='panel_control'),
    path('filtro/', FiltroLibro.as_view(), name='libro_list'),
]