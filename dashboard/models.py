from django.db import models
# Import User model
from django.contrib.auth.models import User
# Import catalogues models
from catalogues.models import StatusIssue, VideoTutorialStatus, CeoListStatus, PromotersListStatus

# Create your models here.

# Sesion control model
class SesionControl(models.Model):
    sesion = models.CharField(max_length=254, verbose_name='Sesion')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')

    class Meta:
        verbose_name = 'Control de sesion'
        verbose_name_plural = 'Control de sesiones'

    def __str__(self):
        return "Sesion de %s" % (self.user.get_full_name())

# Information Issues model
class InformationIssue(models.Model):
    title = models.CharField(max_length=254, verbose_name='Titulo')
    message = models.TextField(verbose_name='Mensaje')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    upstream_promoter = models.CharField(max_length=254, verbose_name='Promotor ascendente')
    status_issue = models.ForeignKey(StatusIssue, on_delete=models.CASCADE, verbose_name='Status', default=1)

    class Meta:
        verbose_name = 'Correccion de data'
        verbose_name_plural = 'Correcciones de data'

    def __str__(self):
        return "Mensaje de %s" % (self.user.get_full_name())


# Video tutorial header model
class VideoTutorialsHeader(models.Model):
    titulo = models.CharField(max_length=255, verbose_name='Titulo')
    descripcion = models.TextField(verbose_name='Descripcion')
    image_tuturial = models.ImageField(verbose_name='Imagen de categoria')
    status = models.ForeignKey(VideoTutorialStatus, on_delete=models.CASCADE, verbose_name='Status')

    class Meta:
        verbose_name = 'Categoria de tutorial'
        verbose_name_plural = 'Categorias de tutoriales'

    def __str__(self):
        return self.titulo

#Video Tutorial model
class VideoTutorials(models.Model):
    titulo = models.CharField(max_length=255, verbose_name='Titulo')
    descripcion = models.TextField(verbose_name='Descripcion')
    video = models.URLField(verbose_name='Video', null=True, blank=True)
    files = models.FileField(verbose_name='Archivos', null=True, blank=True)
    videoheader = models.ForeignKey(VideoTutorialsHeader, on_delete=models.CASCADE, verbose_name='Categoria', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado', null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='Modificado', null=True, blank=True)
    status = models.ForeignKey(VideoTutorialStatus, on_delete=models.CASCADE, verbose_name='Status')

    class Meta:
        verbose_name = 'Video tutorial'
        verbose_name_plural = 'Video tutoriales'

    def __str__(self):
        return "Video de %s" % (self.titulo)


# Registro de directores
class CeosRegisterList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Director')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado', null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='Modificado', null=True, blank=True)
    status = models.ForeignKey(CeoListStatus, on_delete=models.CASCADE, verbose_name='Status')

    class Meta:
        verbose_name = 'Director'
        verbose_name_plural = 'Directores'

    def __str__(self):
        return self.user.get_full_name()


# Registro de socios ascendentes
class PromotersRegisterList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Socio ascendente')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado', null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='Modificado', null=True, blank=True)
    status = models.ForeignKey(PromotersListStatus, on_delete=models.PROTECT, verbose_name='Status')

    class Meta:
        verbose_name = 'Socio ascendente'
        verbose_name_plural = 'Socio ascendente'

    def __str__(self):
        return self.user.get_full_name()
