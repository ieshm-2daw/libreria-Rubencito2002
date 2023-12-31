from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    dni = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.username

class Autor(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank = True)
    bibliografia = models.TextField()
    foto = models.ImageField(upload_to='autores/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Editorial(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    web = models.URLField()

    def __str__(self):
        return self.nombre

# class Genero(models.Model):
#     nombre = models.CharField(max_length = 100, null=True, blank = True)

#     def __str__(self):
#         return self.nombre

class Libro(models.Model):
    DISPONIBILIDAD = (
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('en_proceso', 'En proceso de préstamo'),
    )

    titulo = models.CharField(max_length=255, null=True, blank = True)
    autores = models.ManyToManyField(Autor)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    fecha_publicacion = models.DateField()
    genero = models.CharField(max_length=255, null=True, blank = True)
    isbn = models.CharField(max_length=13)
    resumen = models.TextField()
    disponibilidad = models.CharField(max_length=20, choices=DISPONIBILIDAD, default='disponible')
    portada = models.ImageField(upload_to='portadas/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

class Prestamos(models.Model):
    ESTADO = (
        ('prestado','Prestado'),
        ('devuelto','Devuelto'),
    )

    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO, default='prestado')

    def __str__(self):
        return f"Prestamo de {self.libro.titulo} a {self.usuario}"

class Valoracion(models.Model):
    PUNTUACIONES = (
        (0, "0 estrella"),
        (1, "1 estrella"),
        (2, "2 estrella"),
        (3, "3 estrella"),
        (4, "4 estrella"),
        (5, "5 estrella"),
    )

    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(choices=PUNTUACIONES, default=0)
    comentario = models.TextField(blank=True, null=True)
    fecha_valoracion = models.DateField()

    def __str__(self):
        return f"{self.usuario.username} - {self.libro.titulo} ({self.puntuacion} estrellas)"