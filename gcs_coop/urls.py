"""gcs_coop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
# Import handler for 404 & 500 errors
from django.conf.urls import handler404, handler500
# Import own error templates
from core.views import error404template, error500template


urlpatterns = [
    # URLS from App registration
    path('accounts/', include('django.contrib.auth.urls')),

    # URLS from Django admin
    path('admin/', admin.site.urls),

    # URLS from App Core
    path('', include('core.urls')),

    # URLS from App dashboard
    path('dashboard/', include('dashboard.urls')),

    # URLS from App process_socio
    path('process_coop/', include('process_coop.urls')),

    # URLS from App nuevo proceso (pre-registro)
    path('new-register/', include('pre_register.urls')),

    # URLS from App runway
    path('runway/', include('runway.urls')),
]

# Change the view to show error template
handler404 = error404template
handler500 = error500template

# Comprobar si el Debug está en marcha o desactivado
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)