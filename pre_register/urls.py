from django.urls import path
from . import views

# URLS from App Pre-register

urlpatterns = [
    # Nuevo registro de socio
    path('', views.pre_create_user, name='new_register'),

    # Información de identificación
    path('identificacion-socio/<int:id_user>/', views.pre_identify_info, name='pre_identify_info'),

    # Información general
    path('datos-generales/<int:id_user>/', views.pre_general_info, name='pre_general_info'),

    # Información de dirección
    path('datos-direccion/<int:id_user>/', views.pre_address_registration, name='pre_address_registration'),

    # Numeros de contacto
    path('numeros-de-contacto/<int:id_user>/', views.pre_numbers_registration, name='pre_numbers_registration'),

    # Correos alternativos
    path('correo-alternativo/<int:id_user>/', views.pre_alternative_emails, name='pre_alternative_emails'),

    # Datos de cotizacion
    path('cotizacion/<int:id_user>/', views.pre_imss, name='pre_imss'),

    # Actividades economicas
    path('actividad-economica/<int:id_user>/', views.pre_economic_act, name='pre_economic_act'),

    # Comisiones del socio
    path('comisiones/<int:id_user>/', views.pre_data_bnk_rec, name='pre_databnk_rec'),

    # Dependientes economicos
    path('dependientes-economicos/<int:id_user>/', views.pre_economic_dependent, name='pre_economic_depen'),

    # Referencias personales
    path('referencias-personales/<int:id_user>/', views.pre_personal_references, name='pre_personal_ref'),

    # Resumen de información
    path('resumen-informacion/<int:id_user>/', views.pre_resumen, name='pre_resumen'),
]
