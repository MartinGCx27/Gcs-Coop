from django.urls import path
from . import views

# URLS from App Core

urlpatterns = [
    # Home
    path('', views.gcs_home, name='home'),

    # Filosofia
    path('filosofy/', views.filosofy, name='filosofy'),

    # Beneficios
    path('benefits/', views.benefits, name='benefits'),

    # Revista digital
    path('magazine/', views.magazine, name='magazine'),

    # Proceso
    path('process/', views.process, name='process'),

    # Seguridad social
    path('social_security/', views.social_security, name='social_security'),

    # Modalidad 40
    path('modality_40/', views.modality_40, name='modality_40'),

    # Pensiones
    path('pension/', views.pension_97, name='pension_97'),

    # Promotor
    path('promoter/', views.promoter, name='promoter'),

    # Contacto
    path('contact/', views.contact, name='contact'),

    # Mensaje enviado
    path('message_sended/', views.message_ok, name='message_ok'),

    # Development site
    path('weareworking/', views.working, name='working'),

    # Gcs-Arquitectos
    path('arquitectos/', views.gcs_arquitectos, name='gcs_arquitectos')
]
