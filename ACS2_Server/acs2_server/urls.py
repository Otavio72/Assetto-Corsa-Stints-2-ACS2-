"""
URL configuration for acs2_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from telemetry.views import *
from django.urls import path, include
from telemetry import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/teste/', teste),
    path('', views.index, name='index'), # Pagina INICIAL
    path('index/', views.index, name='index'), # Pagina principal
    
    path('AssettoCorsa/', views.AssettoCorsa, name='AssettoCorsa'),
    path('f12013/', views.f12013, name='f12013'),
    path('motorsportmanager/', views.motorsportmanager, name='motorsportmanager'),

    path("analise/<str:game>/<int:stint_a>/<int:stint_b>/", views.analise, name="analise"),
    path('about/', views.about, name='about'), # Pagina "Quem somos"
    path('usuarios/', include('usuarios.urls')), # Rotas relacionadas a usuários (login, cadastro, perfil)
]
