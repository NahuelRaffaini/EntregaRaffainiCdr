from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.contrib.auth.models import User


def cv_upload_to(instance, filename):
    return f'archivos/cv/{filename}'

def pdf_upload_to(instance, filename):
    return f'archivos/pdf/{filename}'

# Create your models here.
class Proyecto(models.Model):

    titulo = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=500)
    link = models.URLField(max_length=256)
    pdf = models.FileField(upload_to=pdf_upload_to)
    email = models.EmailField()
    inversion = models.CharField(max_length=40)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)



    def __str__(self):
        return f'{self.titulo}'

class Trabajador(models.Model):

    PUESTO_CHOICES = [
    (1, 'Obrero'),
    (2, 'Maestro mayor'),
    (3, 'Arquitecto'),
    (4, 'Ingeniero'),
    (5, 'Renderista'),
    (6, 'Maquetista'),
    (7, 'Otro'),
    ]

    HORARIO_CHOICES = [
    (1, 'Mañana'),
    (2, 'Tarde'),
    (3, 'Total'),
    ]

    DISPONIBILIDAD_CHOICES = [
    (1, 'Semana'),
    (2, 'Fin de Semana'),
    (3, 'Total'),
    ]

    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    numero = models.CharField(max_length=30)
    email = models.EmailField()
    cv = models.FileField(upload_to=cv_upload_to, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg'])])
    puesto = models.IntegerField(choices=PUESTO_CHOICES)
    horario = models.IntegerField(choices=HORARIO_CHOICES, default=3)
    disponibilidad = models.IntegerField(choices=DISPONIBILIDAD_CHOICES, default=3)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Material(models.Model):

    nombre = models.CharField(max_length=40)
    numero = models.CharField(max_length=30)
    email = models.EmailField()
    barrio = models.CharField(max_length=40, blank=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Mensaje(models.Model):

    remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_enviados')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    eliminado = models.BooleanField(default=False)


    def __str__(self):
        return f'De {self.remitente} a {self.destinatario}'