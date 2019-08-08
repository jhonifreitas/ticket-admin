"""IPTVAdmin URL Configuration

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
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

# Admin customization.
admin.site.site_header = 'Painel IPTV'
admin.site.site_title = 'Painel IPTV'
admin.site.index_title = 'Administração'


urlpatterns = [
    path('admin/', admin.site.urls),

    # Home
    path('', include('IPTVAdmin.core.urls', namespace='core')),

    # Usuarios
    path('usuario/', include('IPTVAdmin.custom_profile.urls', namespace='profile')),

    # Boletos
    path('boleto/', include('IPTVAdmin.billet.urls', namespace='billet')),
]

if settings.DEFAULT_FILE_STORAGE == 'django.core.files.storage.FileSystemStorage':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
