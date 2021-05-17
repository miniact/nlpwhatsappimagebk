"""djangonlp_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.urls.conf import include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #Oauth
    path('api/magicauth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('api/user/', include('users.urls', namespace='users')),

    path('admin/', admin.site.urls),
    #ads api
    path('', include('ads.urls', namespace='ads')),
    path('api/ads/', include('ads_api.urls', namespace='ads_api') ),
    path('api/chat/', include('chatnlp.urls', namespace='chat_api')),
    path('djangonlp-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('startnlpprocessing',)
# rest login logout 
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
