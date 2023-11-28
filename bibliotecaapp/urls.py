from django.urls import path
from . import views
from .views import Listado, Details, Edit, Delete

urlpatterns = [
    path('', Listado.as_view(), name='listado'),
    path('details/<int:pk>', Details.as_view(), name='details'),
    path('edit/<int:pk>/', Edit.as_view(), name='update'),
    path('delete/<int:pk>/', Delete.as_view(), name='delete')
]
