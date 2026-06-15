from django.apps import AppConfig

# Configuração da aplicação 'usuarios' para o Django
class UsuariosConfig(AppConfig):
    
    # Define o tipo padrão para os campos auto incrementais (primary key) como BigAutoField (inteiro grande)
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nome da aplicação
    name = 'usuarios'
