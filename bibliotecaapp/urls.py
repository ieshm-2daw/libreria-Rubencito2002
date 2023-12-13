from django.urls import path
from . import views
from .views import ListadoBook, ListadoPrestado, DetailsBook, EditBook, DeleteBook, CreateBook, Realizar_Prestamo, Devolver_Prestamo

urlpatterns = [
    path('', ListadoBook.as_view(), name='listado'),
    path('listadoPrestado', ListadoPrestado.as_view(), name='listado_prestado'),
    path('details/<int:pk>', DetailsBook.as_view(), name='details'),
    path('edit/<int:pk>/', EditBook.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteBook.as_view(), name='delete'),
    path('created/', CreateBook.as_view(), name='created'),
    path('prestamo/<int:pk>/', Realizar_Prestamo.as_view(), name='realizar_prestamo'),
    path('devolucion/<int:pk>/', Devolver_Prestamo.as_view(), name='devolver_prestamo'),
<<<<<<< HEAD
]
=======
]
>>>>>>> ff57fecf71db5c4d366940bef4cca4cfbebc1a00
