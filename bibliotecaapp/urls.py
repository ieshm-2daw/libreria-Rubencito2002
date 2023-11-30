from django.urls import path
from . import views
from .views import ListadoBook, DetailsBook, EditBook, DeleteBook, CreateBook, Prestamo

urlpatterns = [
    path('', ListadoBook.as_view(), name='listado'),
    path('details/<int:pk>', DetailsBook.as_view(), name='details'),
    path('edit/<int:pk>/', EditBook.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteBook.as_view(), name='delete'),
    path('created/', CreateBook.as_view(), name='created'),
    path('prestamo/<int:pk>/', Prestamo.as_view(), name='prestamo'),
]
