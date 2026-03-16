from django.urls import path
from . import views
from .views import Pmnt_validator

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # My info
    path('my_infor/', views.my_info, name='my_info'),

    # Issue message sended
    path('issue_sended/', views.issue_sended, name='issue_sended'),

    # Update Information issue
    path('update_info_issue/<int:id_issue>/', views.update_info_issue, name='update_info_issue'),

    # Issue message recived
    path('info_recived/', views.info_recived, name='info_recived'),

    # Message
    path('message/', views.message, name='message'),

    # View User information
    path('v_info_user/<int:id_user>', views.v_info_user, name='v_info_user'),

    # C_Sercies
    path('services/', views.services, name='services'),

    # Create services
    path('create_service/', views.create_service, name='create_service'),

    # Update Service
    path('update_service/<int:id_service>/', views.update_service, name='update_service'),

    # Pre-register list
    path('pre_register_list/', views.pre_register_list, name='pre_register_list'),

    # Pre-register information
    path('pre_register_view/<int:id_user>/', views.v_pre_user, name='v_pre_user'),

    # Tutorials view
    path('tutorials/process/<int:id_category>/', views.tuto_process, name='tuto_process'),

    # Oficial pages
    path('oficial_pages/', views.oficial_pages, name='oficial_pages'),

    # Downloads
    path('downloads/', views.downloads, name='downloads'),

    # Related videos view
    path('related_videos/', views.related_videos, name='related_videos'),

    # Digital magazine view
    path('digital_magazine/', views.digital_magazine, name='digital_magazine'),

    # # Pmnt_validator view
    # path('pmnt_validator/<int:id_user>/', views.pmnt_validator, name='pmnt_validator'),
    # Pmnt_validator class view
    path('pmnt_validator/<int:id_user>/', Pmnt_validator.as_view(), name='pmnt_validator'),

    # Register link
    path('invitation-code/', views.invitation_code, name='invitation_code')
]
