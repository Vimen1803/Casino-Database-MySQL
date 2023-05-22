import os
import sys
import subprocess
import mysql.connector
from decouple import config

if len(sys.argv) > 1:
    correo_user = sys.argv[1]

os.system("cls")

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

consulta_username = "SELECT username FROM usuarios WHERE correo = %s"
cursor.execute(consulta_username, (correo_user,))
username = cursor.fetchone(); username = username[0]

consulta_tag = "SELECT tag FROM usuarios WHERE correo = %s"
cursor.execute(consulta_tag, (correo_user,))
tag = cursor.fetchone(); tag = tag[0]

consulta_dinero = "SELECT dinero FROM usuarios WHERE correo = %s"
cursor.execute(consulta_dinero, (correo_user,))
dinero = cursor.fetchone(); dinero = dinero[0]

consulta_wins_rps =  "SELECT partidas_rps_wins FROM usuarios WHERE correo = %s"
cursor.execute(consulta_wins_rps, (correo_user,))
wins_RPS = cursor.fetchone(); wins_RPS = wins_RPS[0]

consulta_partidas_rps =  "SELECT partidas_rps_totales FROM usuarios WHERE correo = %s"
cursor.execute(consulta_partidas_rps, (correo_user,))
partidas_RPS = cursor.fetchone(); partidas_RPS = partidas_RPS[0]

consulta_dinero_rps =  "SELECT rps_dinero FROM usuarios WHERE correo = %s"
cursor.execute(consulta_dinero_rps, (correo_user,))
dinero_RPS = cursor.fetchone(); dinero_RPS = dinero_RPS[0]

consulta_wins_tragaperras =  "SELECT partidas_tragaperras_wins FROM usuarios WHERE correo = %s"
cursor.execute(consulta_wins_tragaperras, (correo_user,))
wins_tragaperras = cursor.fetchone(); wins_tragaperras = wins_tragaperras[0]

consulta_partidas_tragaperras =  "SELECT partidas_tragaperras_totales FROM usuarios WHERE correo = %s"
cursor.execute(consulta_partidas_tragaperras, (correo_user,))
partidas_tragaperras = cursor.fetchone(); partidas_tragaperras = partidas_tragaperras[0]

consulta_dinero_tragaperras =  "SELECT tragaperras_dinero FROM usuarios WHERE correo = %s"
cursor.execute(consulta_dinero_tragaperras, (correo_user,))
dinero_tragaperras = cursor.fetchone(); dinero_tragaperras = dinero_tragaperras[0]

consulta_dinero_ruleta =  "SELECT ruleta_dinero FROM usuarios WHERE correo = %s"
cursor.execute(consulta_dinero_ruleta, (correo_user,))
dinero_ruleta = cursor.fetchone(); dinero_ruleta = dinero_ruleta[0]

dinero_total = dinero_tragaperras + dinero_ruleta + dinero_RPS

print(f"Bienvenido {username}\n\n")


def eleccion():
    opcion = int(input("Este es el menú del casino, tienes distintos juegos y opciones.\nPulse 0 para salir.\nPulse 1 para cambiar de cuenta.\nPulse 2 para ver la información de tu perfil.\nPulse 3 para jugar RPS.\nPulse 4 para jugar a las tragaperras.\nPulse 5 para jugar a la ruleta.\n\n"))

    if opcion == 0:
        quit()
    elif opcion == 1:
        ruta = os.path.join("index.py")
        subprocess.run(["python", ruta])
    elif opcion == 2:
        print(f"\n\nCódigo de usuario: {tag}.\nCorreo electrónico: {correo_user}\nUsername: {username}\nDinero disponible: {dinero}€\n\nJUEGOS:\n\nRPS:\n-Partidas: {wins_RPS}/{partidas_RPS}\n-Dinero invertido: {dinero_RPS}€\n\nTragaperras:\n-Partidas: {wins_tragaperras}/{partidas_tragaperras}\n-Dinero invertido: {dinero_tragaperras}€\n\nRuleta:\n-Dinero invertido: {dinero_ruleta}€\n\nDINERO TOTAL GASTADO: {dinero_total}€\n\n\n")

        eleccion()
    elif opcion == 3:
        iniciar_RPS(correo_user)
    elif opcion == 4:
        iniciar_tragaperras(correo_user)
    elif opcion == 5:
       iniciar_Ruleta(correo_user)

def iniciar_tragaperras(correo_user):
    os.system("cls")
    ruta = os.path.join("Juegos", "Tragaperras.py")
    subprocess.run(["python", ruta, correo_user])

def iniciar_RPS(correo_user):
    os.system("cls")
    ruta = os.path.join("Juegos", "RPS.py")
    subprocess.run(["python", ruta, correo_user])

def iniciar_Ruleta(correo_user):
    os.system("cls")
    ruta = os.path.join("Juegos", "Ruleta.py")
    subprocess.run(["python", ruta, correo_user])

eleccion()
