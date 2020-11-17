"""hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
<<<<<<< HEAD
import MainApp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reserve/', include('RoomApp.urls', namespace="RoomApp")),
    path('', MainApp.views.main, name = "main"),
=======

urlpatterns = [
    path('admin/', admin.site.urls),
    path('userApp/', include('UserApp.urls')),
>>>>>>> e33a92218259f2e50ecb5ff54501dcb492afde62
]
