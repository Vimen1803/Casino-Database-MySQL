import mysql.connector
from mysql.connector import Error
from decouple import config
from datetime import datetime
import re
import os
import random
import string
import smtplib
import subprocess

correo_admin = config("correo_admin")
password = config("password")

server = smtplib.SMTP("smtp.gmail.com", port="587")
server.ehlo()
server.starttls()
server.login(correo_admin,password)

email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$'

host=config("host")
database=config("database")
user=config("user")
password=config("password_sql")

conexion = mysql.connector.connect(
    host=host,
    database=database,
    user=user,
    password=password 
)

cursor = conexion.cursor()

caracteres = string.ascii_letters + string.digits
tag = ''.join(random.choices(caracteres, k=4))
tag = str(tag)
tag = tag.upper()
tag = (f"#{tag}")
dinero = 200
partidas_rps_wins = 0
partidas_rps_totales = 0
partidas_rps_dinero = 0
partidas_tragaperras_wins = 0
partidas_tragaperras_totales = 0
partidas_tragaperras_dinero = 0
dinero_ruleta = 0
fecha_creacion = datetime.now()

print("\n\n---------\nRegistro\n---------\n\n")

def coger_datos(validez):
    global correo_user, usuario, username, pass_user
    correo_user = input(str(f"{validez}Cual es tu gmail? --> " ))
    consulta_existe_correo = "SELECT correo FROM usuarios WHERE correo = %s"
    cursor.execute(consulta_existe_correo, (correo_user,))
    registro = cursor.fetchone()
    if registro is not None:
            eleccion = int(input("\n\nEsta cuenta ya existe, si desea iniciar sesion pulse 0, si desea crear otra cuenta pulse 1\n\n"))
            if eleccion == 0:
                ruta = os.path.join("Usuarios", "Inicio_Sesion.py")
                subprocess.run(["python", ruta])
            elif eleccion == 1:
                coger_datos()
    else:
        if re.match(email_pattern, correo_user):
            entrada = True
        else: 
            entrada = False
            validez = "Correo no valido.¿"
    while entrada == False:
        coger_datos(validez)
        
    usuario = correo_user.lower()

    username = input(str("¿Cual es tu username? --> "))
    while len(username) < 4:
        username = input(str("Usuario no valido.\n¿Cual es tu username? --> "))

    pass_user = input(str("¿Cual es tu contraseña? --> "))
    while len(pass_user) < 8:
        pass_user = input(str("Contraseña no valida.\n¿Cual es tu contraseña? --> "))
        
    enviar_mail()

def enviar_mail():
    codigo = random.randint(100000,999999)
    asunto = "Codigo de verificacion Vimen's app"
    msg = f"Hola {username}!\n\n\nLe enviamos este codigo de verificacion para crear una cuenta en nuestra app.\n\n\nSi usted no ha solicitado ningun codigo por favor, pongase en contacto con nosottos a traves de:\n\n\nvictormnjfan@gmail.com\n\n\nSu codigo secreto es {codigo}\n\n\nMuchas gracias por usar nuestra pagina!!\n\n\nEquipo de asistencia de Vimen."
    msg = "Subject: {}\n\n{}".format(asunto,msg)
    server.sendmail(correo_admin, correo_user, msg)
    
    codigo_usuario = int(input("Se le ha enviado un codigo secreto a la direccion de correo electronico.\nIngrese su codigo secreto --> "))
    if codigo_usuario == codigo:
        guardar_datos()
    else:
        global codigo_usuario2 
        codigo_usuario2 = int(input("Codigo incorrecto, vuelva a intentarlo --> "))
        if codigo_usuario2 == codigo:
            guardar_datos()
        else:
            print("Codigo incorrecto.\n")
            quit()

def guardar_datos():
    consulta_insertar = """INSERT INTO usuarios (Tag, correo, username, password, dinero, partidas_rps_wins, partidas_rps_totales, rps_dinero, partidas_tragaperras_wins, partidas_tragaperras_totales, tragaperras_dinero, ruleta_dinero, fecha_creacion)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    datos = (tag, usuario, username, password, dinero, partidas_rps_wins, partidas_rps_totales, partidas_rps_dinero, partidas_tragaperras_wins, partidas_tragaperras_totales, partidas_tragaperras_dinero, dinero_ruleta, fecha_creacion)

    cursor.execute(consulta_insertar, datos)
    print("Verificacion realizada con exito")
    
    conexion.commit()
    cursor.close()
    conexion.close()
    iniciar_menu(correo_user)

def iniciar_menu(correo_user):
    ruta = os.path.join("src", "Menu.py")
    subprocess.run(["python", ruta, correo_user])

validez = "¿"
coger_datos(validez)