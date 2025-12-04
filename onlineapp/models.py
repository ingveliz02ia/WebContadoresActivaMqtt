from typing import Any
from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth.models import AbstractUser

class user_modificado(AbstractUser):
    #email= models.CharField(blank=True, primary_key=True)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno =  models.CharField(max_length=50)
    nombres = models.CharField(max_length=50)
    telefono = models.CharField(blank=True,max_length=12)
    direccion = models.CharField(max_length = 150) 
    
    #Esta funcion agrupa los datospersonales
    def nombre_completo (self):
        return "{} {},{}". format (self.apellido_paterno, self.apellido_materno, self.nombres)
    
    #Cuando indexamos la tabla con una llave foranea esta nos retorna el str q hemos cambiado
    def __str__ (self):
        return self.nombre_completo()
        
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'Clientes'
        ordering = ['last_name']  
    

class data_chip (models.Model):
    id_chip=  models.BigAutoField(primary_key=True)
    codigo_chip = models.CharField(max_length=12)   
    ubicacion_chip = models.CharField(max_length=50) 
    nombre_local_chip = models.CharField(max_length=50) 
    fecha_reg_chip = models.DateTimeField(default = datetime.datetime.now())
    user_chip = models.ForeignKey(user_modificado, null=True, blank=True, on_delete = models.CASCADE) 
      
    def __str__(self) :
        return self.codigo_chip
        
    class Meta:
        verbose_name='Data de Chip'
        verbose_name_plural='Registro de CIs'
        db_table = 'data_Chip'
        ordering = ['id_chip']  
        
class data_reg (models.Model):
    id_data = models.BigAutoField(primary_key=True)
    codigo_chip = models.CharField (max_length =12)
    cuenta_in1 = models.IntegerField()
    cuenta_in2 = models.IntegerField ()
    cuenta_out1 = models.IntegerField()
    cuenta_out2 = models.IntegerField()    
    crc = models.IntegerField()
    evento = models.CharField (max_length =25)
    estado_relay = models.CharField (max_length =25)
    fecha_data = models.DateTimeField(default = datetime.datetime.now())
    codigo_data = models.ForeignKey(data_chip, null=True, blank=True, on_delete = models.CASCADE)       
        
    class Meta:
        verbose_name='registro'
        verbose_name_plural='Registro de Data'
        db_table = 'data_reg'
        ordering = ['id_data']