from django.urls import path
from . import views

# Define as rotas para as páginas de autenticação e perfil de usuário.
urlpatterns = [
    path('register/', views.register, name='register'), # Página de registro de novo usuário
    path('login/', views.login_view, name='login'), # Página de login
    path('perfil/', views.perfil, name='perfil'), # Página de perfil do usuário autenticado
    path('logout/', views.logout_view, name='logout'), # Encerrar sessão e redirecionar para login
]