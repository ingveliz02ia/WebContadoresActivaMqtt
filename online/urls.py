from django.contrib import admin
from django.urls import path
#Aqui estoy importando todas las categorias
from onlineapp.views import *
from onlineapp import views  # Sin esto marca error views.my_tag
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('', inicio, name="iniciox"),   # Pagina de inicio
    path('inicioT/',inicio, name='iniciox'),
    #Aqui llamo a view llamada consulta y este view llamara a la pagina html
    path('consultaT/',consulta, name='consultax'), 
     path('consulta_chipT/',consulta_chip, name='consultax'), 
    path('graficoT/',grafico, name='graficox'), 
    path('registerT/', register, name='registerx'), 
    path('ingresarT/',LoginView.as_view(template_name = 'ingresar.html' ), name='ingresarx'),
    #path('logoutT/', LogoutView.as_view(template_name = 'inicio.html' ), name='logoutx'),
    #path('logoutT/', LogoutView.as_view(next_page='iniciox'), name='logoutx'),
    path('logoutT/', logout_and_redirect, name='logoutx'),
    #Se Uso este parametro para activar sin resetear la pagina-->
    path('consultaT/Activar_led', Activar, name='ActivarX'),
    path('consultaT/Desactivar_led', Desactivar, name='DesactivarX'),
]
