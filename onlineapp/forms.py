from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#Se agrego esta linea para usar la otra tabla y ya no la tabla auth user, y se cambio los User por CustomUser
from .models import user_modificado

from django.core.exceptions import ValidationError

#class UserForm (UserCreationForm): Con este codigo salia error al correr el programa "ModelForm has no model class specified."
class UserForm (forms.Form):
    username = forms.CharField(label='Ingrese Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Ingresa email')
    apellido_paterno = forms.CharField(label='Ingresa Apellido Paterno', min_length=4, max_length=50)
    apellido_materno = forms.CharField(label='Ingresa Apellido Materno', min_length=4, max_length=50)
    nombres = forms.CharField(label='Ingresa Nombres', min_length=4, max_length=50)
    #first_name = forms.CharField(label='Ingresa Nombres', min_length=4, max_length=150)
    telefono = forms.CharField(label='Ingresa su Número Telefónico', max_length=12)
    password1 = forms.CharField(label='Ingresa password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme password', widget=forms.PasswordInput)
    direccion =  forms.CharField(label='Ingresa la direccion', max_length=255)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = user_modificado.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = user_modificado.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email
    
    def clean_apellido_paterno(self):
        apellido_paterno = self.cleaned_data['apellido_paterno']
        return apellido_paterno   
    
    def clean_apellido_materno(self):
        apellido_materno = self.cleaned_data['apellido_materno']
        return apellido_materno   
    
    def clean_nombres(self):
        nombres = self.cleaned_data['nombres']
        return nombres  
    
    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        return telefono   
    
    def clean_direccion(self):
        direccion = self.cleaned_data['direccion']
        return direccion     

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2
    # De esta manera cuando en view manda a agrabr la infoprmacion, se activa el save y guarda la data , anetriormente no estab bien escrito 
    # solo lo hacia guardando tres valores
    def save(self, commit=True):
        user = user_modificado.objects.create_user(
                username = self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                apellido_paterno=self.cleaned_data['apellido_paterno'],
                apellido_materno=self.cleaned_data['apellido_materno'],
                nombres = self.cleaned_data['nombres'],
                telefono=self.cleaned_data['telefono'],
                password=self.cleaned_data['password1'], 
                direccion=self.cleaned_data['password1'],
        )
        return user