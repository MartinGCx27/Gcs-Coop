from django.db import models
# Import fernet fields
from fernet_fields import EncryptedCharField, EncryptedDateField
# Import catalogues
from catalogues.models import MaritalStatus, MatrimonialRegime, SexList, UserType, AffiliationReason, \
    AffiliateType, StatusUser, StatusReason, OfficesList, NumberType, Natiolanities, LocationCatalogue, \
    StatusImss, ActivityType, AccountType, BnkNames, PaymentMethod, DependentRelation, DependentActivity, \
    ReferenceRelation, PaymentImss, PlaceOfBirth, Status
# Import dashboard models
from dashboard.models import CeosRegisterList, PromotersRegisterList, SesionControl
# Import User model
from django.contrib.auth.models import User


# Create your models here.

# Identify information model
class IdentifyInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, verbose_name='Tipo de usuario')
    affiliation_reason = models.ForeignKey(AffiliationReason, on_delete=models.CASCADE,
                                           verbose_name='Motivo de afiliacion', null=True, blank=True)
    affiliate_type = models.ForeignKey(AffiliateType, on_delete=models.CASCADE, verbose_name='Tipo de afiliacion',
                                       null=True, blank=True)
    status_user = models.ForeignKey(StatusUser, on_delete=models.CASCADE, verbose_name='Status usuario')
    status_reason = models.ForeignKey(StatusReason, on_delete=models.CASCADE, verbose_name='Status motivo')
    offices_list = models.ForeignKey(OfficesList, on_delete=models.CASCADE, verbose_name='Oficina')
    ceo = models.ForeignKey(CeosRegisterList, on_delete=models.CASCADE, verbose_name='Director')
    upstream_promoter = models.ForeignKey(PromotersRegisterList, on_delete=models.PROTECT,
                                          verbose_name='Promotor ascendente')
    status_pmnt_sesion = models.ForeignKey(SesionControl, on_delete=models.CASCADE, verbose_name='Estatus de pago',
                                           null=True, blank=True)

    class Meta:
        verbose_name = 'Información de identificacion'
        verbose_name_plural = 'Información de identificacion'

        db_table = 'coop_info_identifyinformation'

    def __str__(self):
        return "Informacion de %s" % (self.user.get_full_name())


# General information model
class GeneralInformation(models.Model):
    coop_age = models.IntegerField(verbose_name='Edad')
    place_of_birth = models.ForeignKey(PlaceOfBirth, on_delete=models.CASCADE, verbose_name='Lugar de nacimiento')
    date_of_birth = models.DateField(verbose_name='Fecha de nacimiento')
    nationality = models.ForeignKey(Natiolanities, on_delete=models.CASCADE, verbose_name='Nacionalidad', null=True,
                                    blank=True)
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.CASCADE, verbose_name='Estado civil', null=True,
                                       blank=True)
    matrimonial_regime = models.ForeignKey(MatrimonialRegime, on_delete=models.CASCADE,
                                           verbose_name='Regimen matrimonial', null=True, blank=True)
    curp = models.CharField(max_length=254, verbose_name='CURP', null=True, blank=True)
    rfc = models.CharField(max_length=254, verbose_name='RFC', null=True, blank=True)
    sex = models.ForeignKey(SexList, on_delete=models.CASCADE, verbose_name='Sexo', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario', null=True, blank=True)

    class Meta:
        verbose_name = 'Información general'
        verbose_name_plural = 'Información general'

    def __str__(self):
        return "Informacion de %s" % (self.user.get_full_name())


# User Address Model
class UserAddressProcess(models.Model):
    suburb = models.ForeignKey(LocationCatalogue, on_delete=models.CASCADE, verbose_name='Ubicacion')
    street = models.CharField(max_length=254, verbose_name='Calle')
    int_number = models.CharField(max_length=254, verbose_name='Numero interior', null=True, blank=True)
    ext_number = models.CharField(max_length=254, verbose_name='Numero exterior')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')

    class Meta:
        verbose_name = 'Direccion'
        verbose_name_plural = 'Direcciones'

    def __str__(self):
        return self.street


# User number contact model
class NumberContact(models.Model):
    number = models.CharField(max_length=254, verbose_name='Numero')
    number_type = models.ForeignKey(NumberType, on_delete=models.CASCADE, verbose_name='Tipo de numero')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Status', default=1)

    class Meta:
        verbose_name = 'Numero'
        verbose_name_plural = 'Numeros'

    def __str__(self):
        return self.number


# Alternative emails
class AlternativeEmails(models.Model):
    alternative_email = models.CharField(max_length=254, verbose_name='Correo alternativo')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Status', default=1)

    class Meta:
        verbose_name = 'Correo alternativo'
        verbose_name_plural = 'Correos alternativos'

    def __str__(self):
        return self.alternative_email


# Cotizacion IMSS model
class CotizacionImss(models.Model):
    salario_cot = models.ForeignKey(PaymentImss, on_delete=models.CASCADE, verbose_name='Salario')

    class Meta:
        verbose_name = 'Cotizacion IMSS'
        verbose_name_plural = 'Cotizaciones IMSS'

    def __str__(self):
        return str(self.salario_cot)


# Cotizacion IMSS relacion model
class CotImssRelation(models.Model):
    cotizacion_imss = models.ForeignKey(CotizacionImss, on_delete=models.CASCADE, verbose_name='Registro IMSS')
    imss_register_date = models.DateField(verbose_name='Fecha de registro IMSS')
    coti_weeks = models.CharField(max_length=254, verbose_name='Semanas cotizadas')
    status_imss = models.ForeignKey(StatusImss, on_delete=models.CASCADE, verbose_name='Status IMSS')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')

    class Meta:
        verbose_name = 'Cotizacion IMSS relacion'
        verbose_name_plural = 'Cotizacion IMSS relaciones'

    def __str__(self):
        return self.coti_weeks


# Economic activity model
class EconomicActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    activity = models.CharField(max_length=254, verbose_name='Actividad')
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE, verbose_name='Tipo de actividad')
    activity_description = models.TextField(verbose_name='Descripcion de actividad')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Status', default=1)

    class Meta:
        verbose_name = 'Actividad economica'
        verbose_name_plural = 'Actividades economicas'

    def __str__(self):
        return self.activity


# Data bnk rec model
class DataBnkRec(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    bnk_name = models.ForeignKey(BnkNames, on_delete=models.CASCADE, verbose_name='Nombre de banco')
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE, verbose_name='Tipo de cuenta')
    css_name = EncryptedCharField(max_length=254, verbose_name='Nombre de titular')
    css_number = EncryptedCharField(max_length=254, verbose_name='Numero de tarjera', null=True, blank=True)
    css_clave = EncryptedCharField(max_length=254, verbose_name='CLABE', null=True, blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, verbose_name='Forma de pago')

    class Meta:
        verbose_name = 'Datos css rec'
        verbose_name_plural = 'datos css rec'

    def __str__(self):
        return "Datos de %s" % (self.user)


# Economic dependents model
class EconomicDependents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    name = models.CharField(max_length=254, verbose_name='Nombre')
    ape_pat = models.CharField(max_length=254, verbose_name='Apellido paterno')
    ape_mat = models.CharField(max_length=254, verbose_name='Apellido materno')
    relation = models.ForeignKey(DependentRelation, on_delete=models.CASCADE, verbose_name='Parentesco')
    birthdate = models.DateField(verbose_name='Fecha de nacimiento')
    age = models.IntegerField(verbose_name='Edad')
    dependent_activity = models.ForeignKey(DependentActivity, on_delete=models.CASCADE,
                                           verbose_name='Actividad de dependiente')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Status', default=1)

    class Meta:
        verbose_name = 'Dependiente economico'
        verbose_name_plural = 'Dependientes economicos'

    def __str__(self):
        return self.name


# Personal references model
class PersonalReferences(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    name_ref = models.CharField(max_length=254, verbose_name='Nombre')
    ape_pat_ref = models.CharField(max_length=254, verbose_name='Apellido paterno')
    ape_mat_ref = models.CharField(max_length=254, verbose_name='Apellido materno')
    relation = models.ForeignKey(ReferenceRelation, on_delete=models.CASCADE, verbose_name='Relacion')
    meet_time = models.CharField(max_length=254, verbose_name='Tiempo de conocerlo')
    num_contact = models.CharField(max_length=254, verbose_name='Numero de contacto')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Status', default=1)

    class Meta:
        verbose_name = 'Referencia personal'
        verbose_name_plural = 'Referencias personales'

    def __str__(self):
        return "Referencias de %s" % (self.user)


# Documentation model
class DocumentationUser(models.Model):
    identification = models.FileField(verbose_name='Identificacion', blank=True, null=True)
    identification_reverse = models.FileField(verbose_name='Identificacion reverso', blank=True, null=True)
    address_comp = models.FileField(verbose_name='Comprobante domicilio', blank=True, null=True)
    born_cert = models.FileField(verbose_name='Acta de nacimiento', blank=True, null=True)
    curp = models.FileField(verbose_name='Curp', blank=True, null=True)
    rfc = models.FileField(verbose_name='RFC', blank=True, null=True)
    cot_weeks = models.FileField(verbose_name='Semanas cotizadas', blank=True, null=True)
    contract_coop = models.FileField(verbose_name='Contrato coop', blank=True, null=True)
    contract_user = models.FileField(verbose_name='Contrato socio', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')

    class Meta:
        verbose_name = 'Documentacion'
        verbose_name_plural = 'Documentacion'

    def __str__(self):
        return "Documentos de %s" % (self.user)


# Pre-register log
class PreRegisterLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Status', default=1)

    class Meta:
        verbose_name = 'Pre registro log'
        verbose_name_plural = 'Pre registro log'

    def __str__(self):
        return "Pre registro de %s" % (self.user.get_full_name)
