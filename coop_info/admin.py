from django.contrib import admin
# Import models
from .models import *
# Register your models here.

admin.site.register(IdentifyInformation)
admin.site.register(GeneralInformation)
admin.site.register(UserAddressProcess)
admin.site.register(NumberContact)
admin.site.register(AlternativeEmails)
admin.site.register(CotizacionImss)
admin.site.register(CotImssRelation)
admin.site.register(EconomicActivity)
admin.site.register(DataBnkRec)
admin.site.register(EconomicDependents)
admin.site.register(PersonalReferences)
admin.site.register(PreRegisterLog)
admin.site.register(DocumentationUser)
