from django.shortcuts import render, redirect
from .models import data_reg
from .models import user_modificado
from django.contrib.auth.forms import UserCreationForm
from onlineapp.forms import UserForm
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import HttpResponse, QueryDict # No se uso finalmente
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation
import os
from dotenv import load_dotenv

load_dotenv()
BROKER = os.getenv("MQTT_HOST")
PORT = int(os.getenv("MQTT_PORT"))
USER = os.getenv("MQTT_USER")
PASSWORD = os.getenv("MQTT_PASSWORD")
TOPICO = os.getenv("MQTT_TOPIC")

codigochip = "xx" #variable global 
#contexto='xy'

def logout_and_redirect(request):
    logout(request)  # cierra sesión
    return redirect('iniciox')  # redirige a tu inicio

def inicio (request):
    #if request.method == 'POST':
        return render (request, "inicio.html")
    #else:    
       # return render ()
def grafico (request):
    #if request.method == 'POST':
        return render (request, "grafico.html")
    #else:    
       # return render ()       

def registros (request):
    registroListados =  data_reg.objects.all()
    
    return render (request, "pag_registros.html", {"registro_conectahtml": registroListados})

def consulta (request):      
    from django.db import connection 
    
    if request.user.is_authenticated:
        print("User is logged in :)")
        print(f"Username --> {request.user.username}")
        
    else:
        print("User is not logged in :(") 
    
    #Usando el metodo post empezo a salir fallas
    x =request.POST.get('Nro_de_datos')
    print(x)
    global codigochip
    
    codigochip = request.GET.get('codchip_extraido') # cambiamos el valor de la variable global codigochip
       
    NoneType = type(None)  
    if x is None:
        x=50
    else:
        pass
    cantidad=int(x)
    type (cantidad)
    print(cantidad)
    with connection.cursor() as cursor:
        #data = request.user.username # Ya no necesito este filtrado porque con el codigo de chi p s e filtra todo
        query = """
                SELECT 
                    dr.id_data, 
                    dr.codigo_chip AS codigo_chip_reg, 
                    dr.cuenta_in1, 
                    dr.cuenta_in2, 
                    dr.cuenta_out1, 
                    dr.cuenta_out2, 
                    dc.nombre_local_chip, 
                    dc.ubicacion_chip,
                    dr.estado_relay,
                    dr.evento, 
                    dr.fecha_data
                FROM data_reg dr
                INNER JOIN data_Chip dc ON dr.codigo_data_id = dc.id_chip
                INNER JOIN Clientes c ON dc.user_chip_id = c.id
                WHERE dc.codigo_chip = %s
                ORDER BY dr.fecha_data DESC
                """; 
        cursor.execute (query, [codigochip]) # Esta es la forma de llevar una variable dentro de cursor.execute en este caso el usuario de sesion
        rawData = cursor.fetchall()
        result=[]
        ID=[]
        TempA=[]
        TempO=[]
        Con_in=[]
        Con_out=[]
        
        for r in rawData:
            result.append (list(r))
        for r in rawData:
            ID.append (r[0])        
        for r in rawData:
            TempA.append (r[2])
        for r in rawData:
            TempO.append (r[3])    
        for r in rawData:
            Con_in.append (r[4]) 
        for r in rawData:
            Con_out.append (r[5]) 
               
        resultx=result[:cantidad]        
        IDx = ID[:50]
        TempAx = TempA [:50]
        TempOx =TempO[:50]
        Con_inx=Con_in[:50]
        Con_outx=Con_out[:50]
        contexto = {'consultas':resultx, 'id':IDx, 'tempA':TempAx,'tempO':TempOx, 'con_in':Con_inx, 'con_out': Con_outx } # De esa manera se lleva data a la pagina web
       
    return render (request, "consulta.html", contexto)

def consulta_chip (request):      
    from django.db import connection 
    
    if request.user.is_authenticated:
        print("User is logged in :)")
        print(f"Username --> {request.user.username}")
        
    else:
        print("User is not logged in :(") 
    
    
    with connection.cursor() as cursor:
        data = request.user.username 
        query = """ SELECT id_chip, codigo_chip, nombre_local_chip, ubicacion_chip, fecha_reg_chip
                FROM Clientes INNER JOIN data_Chip ON  Clientes.id = data_Chip.user_chip_id 
                WHERE Clientes.username = %s order by  fecha_reg_chip desc""";
        
        cursor.execute (query, [data]) # Esta es la forma de llevar una variable dentro de cursor.execute en este caso el usuario de sesion
        rawData = cursor.fetchall()
        result=[]
        cod_chip=[]
        
        for r in rawData:
            result.append (list(r))  
        
        for r in rawData:
            cod_chip.append (r[1])       
        cod_chipx = cod_chip[:]         
        contexto = {'consulta_chips':result, 'cod_chipxs':cod_chipx} # De esa manera se lleva data a la pagina web
            
    return render (request, "consulta_chip.html", contexto)
    
def register (request):
    if request.method == 'POST':
       form = UserForm (request.POST)
       if form.is_valid():
           form.save()
           username = form.cleaned_data ['username']
           messages.success(request, f'Usuario {username} creado')
           return redirect ('/ingresarT/')
    else:
        form = UserForm ()   
    context ={'form' : form}
    return render (request, "register.html",context)
# No se podia disparar esta accion sin resetear la pagina, queriamos q fuese asincrona
# Se uso los suiguientes  paramrtros

def Activar (request):
    print("Activando señal de encendido")
    import ssl
    import paho.mqtt.client as mqtt
    from django.http import HttpResponse
    from django.contrib import messages
    import time

    tok = TOPICO+"/"
    toker=str(codigochip)
    MENSAJE = tok + toker
    try:
        print(">>> Publicando en topic:", MENSAJE)
        client = mqtt.Client()
        client.username_pw_set(USER, PASSWORD)
        client.tls_set(cert_reqs=ssl.CERT_NONE)
        client.tls_insecure_set(True)
        client.connect(BROKER, PORT, keepalive=60)
        # NECESARIO PARA QUE SE ENVÍE EL MENSAJE
        client.loop_start()
        result = client.publish(MENSAJE, "ON")
        time.sleep(0.2)   # Espera mínima para garantizar envío
        client.loop_stop()
        messages.success(request, "Se activó el relay correctamente")
        print("MQTT → Mensaje enviado: ON")
    except Exception as e:
        print("MQTT → Error:", e)
        messages.error(request, "No se pudo conectar al Broker MQTT")
    return HttpResponse("1")

def Desactivar (request):
    print("Desactivando señal de encendido")
    import ssl
    import paho.mqtt.client as mqtt
    from django.http import HttpResponse
    from django.contrib import messages
    import time

    tok = TOPICO+"/"
    toker=str(codigochip)
    MENSAJE = tok + toker
    try:
        print(">>> Publicando en topic:", MENSAJE)
        client = mqtt.Client()
        client.username_pw_set(USER, PASSWORD)
        client.tls_set(cert_reqs=ssl.CERT_NONE)
        client.tls_insecure_set(True)
        client.connect(BROKER, PORT, keepalive=60)
        # NECESARIO PARA QUE SE ENVÍE EL MENSAJE
        client.loop_start()
        result = client.publish(MENSAJE, "OFF")
        time.sleep(0.2)   # Espera mínima para garantizar envío
        client.loop_stop()
        messages.success(request, "Se Desactivó el relay correctamente")
        print("MQTT → Mensaje enviado: OFF")
    except Exception as e:
        print("MQTT → Error:", e)
        messages.error(request, "No se pudo conectar al Broker MQTT")
    return HttpResponse("1")