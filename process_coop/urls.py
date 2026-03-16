from django.urls import path
from . import views

urlpatterns = [
    # Create user
    path('', views.create_user, name='create_user'),
    # Update user
    path('update_user/<int:id_user>/', views.update_user, name='update_user'),

    # Identify info
    path('identify_info/<int:id_user>/', views.identify_info, name='identify_info'),
    # Update identify
    path('update_identify/<int:id_user>/', views.update_identify_info, name='update_identify'),

    # General information
    path('general_info/<int:id_user>/', views.general_info, name='general_info'),
    # Update general
    path('update_general/<int:id_user>/', views.update_general_info, name='update_general_info'),

    # Address registration
    path('address_registrarion/<int:id_user>/', views.address_registration, name='address_registration'),
    # Update address
    path('update_address/<int:id_user>/', views.update_address, name='update_address'),

    # Numbers registration
    path('numbers_registration/<int:id_user>/', views.numbers_registration, name='numbers_registration'),
    # Matrix numbers
    path('m_numbers/<int:id_user>/', views.m_number_registration, name='m_numbers'),
    # Update numbers
    path('update_numbers/<int:id_number>/', views.update_number_registration, name='update_numbers'),

    # Alternative emails
    path('alternative_emails/<int:id_user>/', views.alternative_emails, name='alternative_emails'),
    # Update alternative emails
    path('update_alternative_emails/<int:id_user>/', views.update_alternative_emails, name='update_alternative_emails'),

    # IMSS info
    path('imss_info/<int:id_user>/', views.imss_info, name='imss_info'),
    # Update IMSS info
    path('update_imss_info/<int:id_user>/', views.update_imss_info, name='update_imss_info'),


    # Economic activity
    path('economic_act/<int:id_user>/', views.economic_act, name='economic_act'),
    # Matrix economic activity
    path('m_economic_activity/<int:id_user>/', views.m_economic_activity, name='m_economic_activity'),
    # Update economic activity
    path('update_economic_activity/<int:id_act>/', views.update_economic_activity, name='update_economic_activity'),

    # Data bnk rec
    path('data_bnk_rec/<int:id_user>/', views.data_bnk_rec, name='data_bnk_rec'),
    # Update Bnk rec
    path('update_bnkrec/<int:id_user>/', views.update_bnkrec, name='update_bnkrec'),

    # Economic dependent
    path('economic_dependent/<int:id_user>/', views.economic_dependent, name='economic_dependent'),
    # Matrix economic dependent
    path('m_economic_dependent/<int:id_user>/', views.m_economic_dependent, name='m_economic_dependent'),
    # Update economic dependent
    path('update_economic_dependent/<int:id_dep>/', views.update_economic_dependent, name='update_economic_dependent'),

    # Personal references
    path('personal_reference/<int:id_user>/', views.personal_references, name='personal_reference'),
    # Matrix personal references
    path('m_update_references/<int:id_user>/', views.m_update_references, name='m_update_references'),
    # Update personal references
    path('update_personal_references/<int:id_ref>/', views.update_personal_references, name='update_personal_references'),

    # Contract user
    path('contract_user/<int:id_user>/', views.contract_user, name='contract_user'),
    # Update contracts
    path('update_contract_user/<int:id_user>/', views.update_contract_user, name='update_contract_user'),

    # Documentation
    path('documentation/<int:id_user>/', views.documentation, name='documentation'),
    # Update Documentation
    path('update_documentation/<int:id_user>/', views.update_documentation, name='update_documentation'),

    # Short register
    path('nuevo-registro/', views.qr_register, name='qr_register'),
    # Short register link
    path('nuevo-registro/<str:optional_nss>/', views.qr_register, name='qr_register_link'),
    # Short register successfully
    path('qr_register_success/', views.qr_register_success, name='qr_register_success'),
]
