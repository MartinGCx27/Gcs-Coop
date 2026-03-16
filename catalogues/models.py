from django.db import models


# Create your models here.

# Services Status model
class StatusServices(models.Model):
    status = models.CharField(max_length=50, verbose_name='Status')

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'

    def __str__(self):
        return self.status


# User Status model
class StatusUser(models.Model):
    status_user = models.CharField(max_length=254, verbose_name='Estatus de usuario')

    class Meta:
        verbose_name = 'Status de usuario'
        verbose_name_plural = 'Status de usuarios'

    def __str__(self):
        return self.status_user


# Reason status
class StatusReason(models.Model):
    statusreason = models.CharField(max_length=254, verbose_name='Motivo')

    class Meta:
        verbose_name = 'Status Motivo'
        verbose_name_plural = 'Status motivos'

    def __str__(self):
        return self.statusreason


# Status IMSS
class StatusImss(models.Model):
    status_imss = models.CharField(max_length=254, verbose_name='Status IMSS')

    class Meta:
        verbose_name = 'Status IMSS'
        verbose_name_plural = 'Status IMSS'

    def __str__(self):
        return self.status_imss


# Information Issue status
class StatusIssue(models.Model):
    status_issue = models.CharField(max_length=254, verbose_name='Status problema')

    class Meta:
        verbose_name = 'Status problema'
        verbose_name_plural = 'Status problemas'

    def __str__(self):
        return self.status_issue


# Status active/inactive
class Status(models.Model):
    status = models.CharField(max_length=254, verbose_name='Status problema')

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'

    def __str__(self):
        return self.status


# Offices list
class OfficesList(models.Model):
    office_name = models.CharField(max_length=254, verbose_name='Actividad de dependiente')

    class Meta:
        verbose_name = 'Oficina'
        verbose_name_plural = 'Oficinas'

    def __str__(self):
        return self.office_name


# Affiliate type
class AffiliateType(models.Model):
    affiliate_type = models.CharField(max_length=254, verbose_name='Tipo de afiliación')

    class Meta:
        verbose_name = 'Tipo de afiliación'
        verbose_name_plural = 'Tipo de afiliaciones'

    def __str__(self):
        return self.affiliate_type


# Affiliation reason
class AffiliationReason(models.Model):
    affiliattion_reason = models.CharField(max_length=254, verbose_name='Motivo de afiliación')

    class Meta:
        verbose_name = 'Motivo de afiliación'
        verbose_name_plural = 'Motivos de afiliaciones'

    def __str__(self):
        return self.affiliattion_reason


# User type
class UserType(models.Model):
    user_type = models.CharField(max_length=254, verbose_name='Tipo de usuario')

    class Meta:
        verbose_name = 'Tipo de usuario'
        verbose_name_plural = 'Tipos de usuario'

    def __str__(self):
        return self.user_type


# Marital status model
class MaritalStatus(models.Model):
    marital_status = models.CharField(max_length=254, verbose_name='Estado civil')

    class Meta:
        verbose_name = 'Estado civil'
        verbose_name_plural = 'Estado civil'

    def __str__(self):
        return self.marital_status


# Matrimonial regime model
class MatrimonialRegime(models.Model):
    matrimonial_regime = models.CharField(max_length=254, verbose_name='Regimen matrimonial')

    class Meta:
        verbose_name = 'Regimen matrimonial'
        verbose_name_plural = 'Regimen Matrimonial'

    def __str__(self):
        return self.matrimonial_regime


# Sex catalogue model
class SexList(models.Model):
    sex = models.CharField(max_length=254, verbose_name='Sexo')

    class Meta:
        verbose_name = 'Sexo'
        verbose_name_plural = 'Sexos'

    def __str__(self):
        return self.sex


# Address catalogues
class StateList(models.Model):
    state = models.CharField(max_length=254, verbose_name='Estado')

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def __str__(self):
        return self.state


# Location catalogue
class LocationCatalogue(models.Model):
    zip_code = models.CharField(max_length=254, verbose_name='Codigo postal')
    suburb = models.CharField(max_length=254, verbose_name='Colonia')
    delegation = models.CharField(max_length=254, verbose_name='Municipio')
    state = models.CharField(max_length=254, verbose_name='Estado')

    class Meta:
        verbose_name = 'Direccion catalogo'
        verbose_name_plural = 'Direcciones catalogo'

    def __str__(self):
        return self.suburb


# Number type model
class NumberType(models.Model):
    number_type = models.CharField(max_length=254, verbose_name='Tipo de telefono')

    class Meta:
        verbose_name = 'Tipo de telefono'
        verbose_name_plural = 'Tipo de telefonos'

    def __str__(self):
        return self.number_type


# Nationalities model
class Natiolanities(models.Model):
    nationality = models.CharField(max_length=254, verbose_name='Nacionalidad')

    class Meta:
        verbose_name = 'Nacionalidad'
        verbose_name_plural = 'Nacionalidades'

    def __str__(self):
        return self.nationality


# Activity type model
class ActivityType(models.Model):
    activity_number = models.IntegerField(verbose_name='Numero de actividad')
    activity_description = models.TextField(verbose_name='Descripcion de texto')
    type = models.IntegerField(verbose_name='Tipo de actividad')

    class Meta:
        verbose_name = 'Tipo de actividad'
        verbose_name_plural = 'Tipo de actividades'

    def __str__(self):
        return self.activity_description


# Account type model
class AccountType(models.Model):
    account_type = models.CharField(max_length=254, verbose_name='Tipo de cuenta')

    class Meta:
        verbose_name = 'Tipo de cuenta'
        verbose_name_plural = 'Tipo de cuentas'

    def __str__(self):
        return self.account_type


# Bnk name catalogue
class BnkNames(models.Model):
    bnk_name = models.CharField(max_length=254, verbose_name='Nombre de banco')

    class Meta:
        verbose_name = 'Nombre de banco'
        verbose_name_plural = 'Nombres de bancos'

    def __str__(self):
        return self.bnk_name


# Pay methods catalogue
class PaymentMethod(models.Model):
    payment_method = models.CharField(max_length=254, verbose_name='Forma de pago')

    class Meta:
        verbose_name = 'Forma de pago'
        verbose_name_plural = 'Formas de pago'

    def __str__(self):
        return self.payment_method


# Dependent relation catalogue
class DependentRelation(models.Model):
    relation = models.CharField(max_length=254, verbose_name='Parentesco')

    class Meta:
        verbose_name = 'Parentesco'
        verbose_name_plural = 'Parentescos'

    def __str__(self):
        return self.relation


# Reference relation catalogue
class ReferenceRelation(models.Model):
    relation = models.CharField(max_length=254, verbose_name='Relacion')

    class Meta:
        verbose_name = 'Relacion'
        verbose_name_plural = 'Relaciones'

    def __str__(self):
        return self.relation


# Dependent activities catalogue
class DependentActivity(models.Model):
    dependent_activity = models.CharField(max_length=254, verbose_name='Actividad')

    class Meta:
        verbose_name = 'Actividad dependieentes'
        verbose_name_plural = 'Actividades dependientes'

    def __str__(self):
        return self.dependent_activity


# Aportacion IMSS
class PaymentImss(models.Model):
    veces = models.FloatField(verbose_name='Veces')
    diario = models.FloatField(verbose_name='Diario')
    aport_coop = models.FloatField(verbose_name='Aportacion Coop')
    com_prom = models.FloatField(verbose_name='Comiciones promotor')
    aport_letter = models.CharField(max_length=254, verbose_name='Aportacion escrita')

    class Meta:
        verbose_name = 'Catalogo de IMSS'
        verbose_name_plural = 'Catalogo de IMSS'

    def __str__(self):
        return "%s" % (self.veces)


# Catalogues States - Place of birth
class PlaceOfBirth(models.Model):
    state_birth = models.CharField(max_length=254, verbose_name='Lugar de nacimiento')

    class Meta:
        verbose_name = 'Lugar de nacimiento'
        verbose_name_plural = 'Lugares de nacimiento'

    def __str__(self):
        return self.state_birth


class VideoTutorialStatus(models.Model):
    status = models.CharField(max_length=254, verbose_name='Status video')

    class Meta:
        verbose_name = 'Status video'
        verbose_name_plural = 'Status videos'

    def __str__(self):
        return self.status


# Ceo register list status
class CeoListStatus(models.Model):
    status = models.CharField(max_length=254, verbose_name='Status ceo')

    class Meta:
        verbose_name = 'Status ceo'
        verbose_name_plural = 'Status ceos'

    def __str__(self):
        return self.status


# Promoters register list status
class PromotersListStatus(models.Model):
    status = models.CharField(max_length=254, verbose_name='Status promoters')

    class Meta:
        verbose_name = 'Status promoter'
        verbose_name_plural = 'Status promoters'

    def __str__(self):
        return self.status


# Enrollment status
class EnrollmentStatus(models.Model):
    status = models.CharField(max_length=254, verbose_name='Status de inscripcion')

    class Meta:
        verbose_name = 'Estatus de inscripcion'
        verbose_name_plural = 'Estatus de inscripcion'

    def __str__(self):
        return self.status


# Enrollment catalogue
class EnrollmentCatalogue(models.Model):
    enrollment_type = models.CharField(max_length=254, verbose_name='Tipo de inscripcion')
    enrollment_price = models.FloatField(verbose_name='Precio')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='Modificado')
    status = models.ForeignKey(StatusServices, on_delete=models.DO_NOTHING, verbose_name='Estatus', default=1)

    class Meta:
        verbose_name = 'Inscripcion'
        verbose_name_plural = 'Inscripciones'

    def __str__(self):
        return self.enrollment_type

    # def get_stripe_price(self):
    #     return "{}".format(self.enrollment_price * 100)
