from django.contrib import admin
from .models import data_chip, data_reg, user_modificado
from django.contrib.auth.admin import UserAdmin

#class usuariosAdmin(UserAdmin):
   # list_display=('username','email','nombre_completo','telefono','direccion')
#admin.site.register(user_modificado, usuariosAdmin)

# Si abro de esta manera dentro de admin la tabla usuarios  no puedo llenar bien los datos del Usuario, porque el pasword me pide de inmediato, sin validar
@admin.register(user_modificado)
class user_modificado(admin.ModelAdmin):
  list_display=('username','email','nombre_completo','telefono','direccion')  

@admin.register(data_chip)
class data_chip(admin.ModelAdmin):
    list_display=('codigo_chip', 'user_chip','ubicacion_chip','nombre_local_chip','fecha_reg_chip')

@admin.register(data_reg)
class data_registrado(admin.ModelAdmin):
    list_display=('cuenta_in1', 'cuenta_in2','cuenta_out1','cuenta_out2','crc','codigo_chip','evento','fecha_data')
    
