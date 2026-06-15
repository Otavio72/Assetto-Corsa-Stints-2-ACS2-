#from usuarios.models import CustomUser
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

# Formulário de registro de novo usuário. 
# Extende o UserCreationForm padrão do Django, adicionando os campos de primeiro e último nome.
class CustomCreationForm(UserCreationForm):

    # Campos Adicionais para o cadastro
    first_name = forms.CharField(required=True, label='Primeiro Nome')
    last_name = forms.CharField(required=True, label='Último Nome')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove os textos de ajuda padrão
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        # Adiciona a classe CSS 'form-control' para estilização de cada campo
        for field_name in self.fields:
            css_class = 'form-control'

            if field_name == 'email':
                self.fields[field_name].widget.attrs.update({'class':css_class, 'id': 'email'})
            if field_name == 'password1':
                self.fields[field_name].widget.attrs.update({'class':css_class, 'id': 'senha'})
            if field_name == 'password2':
                self.fields[field_name].widget.attrs.update({'class':css_class})
            if field_name == 'username':
                self.fields[field_name].widget.attrs.update({'class':css_class})
            if field_name == 'first_name':
                self.fields[field_name].widget.attrs.update({'class':css_class})
            if field_name == 'last_name':
                self.fields[field_name].widget.attrs.update({'class':css_class})

    # Define os campos que serão exibidos no formulário e o modelo associado
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

