import random
import mysql.connector
from mysql.connector import Error
from decouple import config
import smtplib
import os
import subprocess

os.system("cls")

codigo = random.randint(100000, 999999)

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

correo_admin = config("correo_admin")
password = config("password")

server = smtplib.SMTP("smtp.gmail.com", port=587)
server.ehlo()
server.starttls()
server.login(correo_admin, password)

print("------------------\n INICIO DE SESION\n------------------")

def coger_datos():
    global correo_user
    global username
    correo_user = input("\n¿Ingrese el correo al que desea acceder?--> ")
    correo_user = correo_user.lower()

    consulta_existe_correo = "SELECT correo FROM usuarios WHERE correo = %s"
    cursor.execute(consulta_existe_correo, (correo_user,))
    registro = cursor.fetchone()
    if registro is None:
            seleccion = int(input("\nEsta cuenta no existe.\nSi deseas registrarte pulse 0, si deseas salir pulse 1\n\n"))
            if seleccion == 0:
                ruta = os.path.join("Usuarios", "Registro.py")
                subprocess.run(["python", ruta])
            else:
                quit()
    else:
        consulta_password = "SELECT password FROM usuarios WHERE correo = %s"
        cursor.execute(consulta_password, (correo_user,))
        pass_user = cursor.fetchone()
        pass_user = pass_user[0]
        consulta_username = "SELECT username FROM usuarios WHERE correo = %s"
        cursor.execute(consulta_username, (correo_user,))
        username = cursor.fetchone()
        username = username[0]
        pass_log = input("\nIngrese su contraseña --> ")
        if pass_log == pass_user:
            enviar_mail()
        else:
            print("Contraseña incorrecta")
            quit()

def enviar_mail():
    asunto = "Codigo de verificacion Vimen's app"
    msg = f"Hola {username}!\n\n\nLe enviamos este codigo de verificacion para ingresar a nuestra app.\n\n\nSi usted no ha solicitado ningun codigo por favor, pongase en contacto con nosottos a traves de:\n\n\nvictormnjfan@gmail.com\n\n\nSu codigo secreto es {codigo}\n\n\nMuchas gracias por usar nuestra pagina!!\n\n\nEquipo de asistencia de Vimen."
    msg = "Subject: {}\n\n{}".format(asunto, msg)
    server.sendmail(correo_admin, correo_user, msg)

    codigo_usuario = int(input("\nSe le ha enviado un codigo secreto a la direccion de correo electronico.\nIngrese su codigo secreto --> "))
    if codigo_usuario == codigo:
        iniciar_menu(correo_user)
    else:
        codigo_usuario2 = int(
            input("\nCodigo incorrecto, intentelo de nuevo --> "))
        if codigo_usuario2 == codigo:
            iniciar_menu(correo_user)
        else:
            ruta = os.path.join("..", "index.py")
            subprocess.run(["python", ruta])


def iniciar_menu(correo_user):
    ruta = os.path.join("src", "Menu.py")
    subprocess.run(["python", ruta, correo_user])


coger_datos()