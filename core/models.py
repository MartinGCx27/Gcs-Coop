from django.db import models
#Importing Status models
from catalogues.models import StatusServices

# Create your models here.

# Services model
class GcsServices(models.Model):
    title = models.CharField(max_length=254, verbose_name='Nombre de servicio')
    description = models.TextField(verbose_name='Descripción')
    image_service = models.ImageField(verbose_name='Imágen')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='Modificado')
    status = models.ForeignKey(StatusServices, on_delete=models.CASCADE, verbose_name='Estatus', default=1)

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return self.title

# User Contact model
class UserContact(models.Model):
    first_name = models.CharField(max_length=254, verbose_name='Nombre')
    last_name = models.CharField(max_length=254, verbose_name='Apellidos')
    email = models.CharField(max_length=254, verbose_name='Correo')
    message = models.TextField(verbose_name='Mensaje')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'

    def __str__(self):
        return "Mensaje de %s %s" % (self.first_name, self.last_name)