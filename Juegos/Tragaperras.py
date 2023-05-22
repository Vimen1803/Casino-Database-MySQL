import sys
import subprocess
import random
import os
import mysql.connector
from decouple import config

if len(sys.argv) > 1:
    correo_user = sys.argv[1]

premios = ["V", "B", "C", "D", "E"]
peso = [1,2,2,2,2]

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

def coger_datos(correo_user):
    global dinero, wins_tragaperras, partidas_tragaperras, dinero_tragaperras
    consulta_dinero = "SELECT dinero FROM usuarios WHERE correo = %s"
    cursor.execute(consulta_dinero, (correo_user,))
    dinero_ = cursor.fetchone(); dinero = dinero_[0]

    consulta_wins_tragaperras =  "SELECT partidas_rps_wins FROM usuarios WHERE correo = %s"
    cursor.execute(consulta_wins_tragaperras, (correo_user,))
    wins_tragaperras_ = cursor.fetchone(); wins_tragaperras = wins_tragaperras_[0]

    consulta_partidas_tragaperras =  "SELECT partidas_tragaperras_totales FROM usuarios WHERE correo = %s"
    cursor.execute(consulta_partidas_tragaperras, (correo_user,))
    partidas_tragaperras_ = cursor.fetchone(); partidas_tragaperras = partidas_tragaperras_[0]

    consulta_dinero_tragaperras =  "SELECT tragaperras_dinero FROM usuarios WHERE correo = %s"
    cursor.execute(consulta_dinero_tragaperras, (correo_user,))
    dinero_tragaperras_ = cursor.fetchone(); dinero_tragaperras = dinero_tragaperras_[0]
    calcular_apuesta()     

def calcular_apuesta():
    global apuesta
    apuesta = int(input(f"\nTienes {dinero}€, ¿cuanto dinero deseas apostar? --> "))
    while apuesta > dinero or apuesta <= 0:
        apuesta = int(input(f"\n\nTienes {dinero}€, ¿cuanto dinero deseas apostar? --> "))
    if apuesta <= dinero:
        combinacion()

def combinacion():
    global combinacion1, combinacion2, combinacion3, premio, premio2, premio3, premio4, recompensa
    combinacion1 = random.choice(premios)
    combinacion2 = random.choice(premios)
    combinacion3 = random.choice(premios)
    premio, premio2, premio3, premio4 = False, False, False, False
    if combinacion1 == combinacion2 == combinacion3:
        premio = True
        if combinacion1 == "V":
            premio2 = True
            premio = False
    elif combinacion1 == combinacion2 != combinacion3:
        if combinacion3 == "V":
            premio3 = True
        elif combinacion1 == "V":
            premio4 = True
    elif combinacion1 == combinacion3 != combinacion2:
        if combinacion2 == "V":
            premio3 = True
        elif combinacion1 == "V":
            premio4 = True
    elif combinacion3 == combinacion2 != combinacion1:
        if combinacion1 == "V":
            premio3 = True
        elif combinacion2 == "V":
            premio4 = True

    print(f"\nLa combinacion ha sido: {combinacion1}|{combinacion2}|{combinacion3}")
    if premio == True:
        recompensa = apuesta * 8
        print(f"Has ganado {recompensa}€")
    elif premio2 == True:
            recompensa = apuesta * 20
            print(f"Has ganado {recompensa}€")
    elif premio3 == True:
        recompensa = apuesta * 2
        print(f"Has ganado {recompensa}€")
    elif premio4 == True:
        recompensa = apuesta * 5
        print(f"Has ganado {recompensa}€")
    else:
        recompensa = 0
        print("Has perdido!")

    dar_premio()

def dar_premio():
    global dinero, dinero_tragaperras, partidas_tragaperras, wins_tragaperras
    ganancia = recompensa - apuesta
    dinero += ganancia
    dinero_tragaperras += apuesta
    partidas_tragaperras += 1
    if premio == True or premio2 == True or premio3 == True or premio4 == True:
        wins_tragaperras += 1
    else:
        wins_tragaperras += 0

    guardar_datos(dinero, dinero_tragaperras, partidas_tragaperras, wins_tragaperras)

def guardar_datos(dinero, dinero_tragaperras, partidas_tragaperras, wins_tragaperras): 
    guardar_dinero = "UPDATE usuarios SET dinero = %s WHERE correo = %s"
    cursor.execute(guardar_dinero, (dinero, correo_user))

    guardar_dinero_tragaperras = "UPDATE usuarios SET tragaperras_dinero = %s WHERE correo = %s"
    cursor.execute(guardar_dinero_tragaperras, (dinero_tragaperras, correo_user))

    guardar_partidas_tragaperras = "UPDATE usuarios SET partidas_tragaperras_totales = %s WHERE correo = %s"
    cursor.execute(guardar_partidas_tragaperras, (partidas_tragaperras, correo_user))

    guardar_wins_tragaperras = "UPDATE usuarios SET partidas_tragaperras_wins = %s WHERE correo = %s"
    cursor.execute(guardar_wins_tragaperras, (wins_tragaperras, correo_user))

    conexion.commit()
    pregunta_final()

def pregunta_final():
    respuesta = int(input(f"Tienes {dinero}€.\nSi deseas salir pulse 0.\nSi deseas cambiar la apuesta pulse 1.\nSi deseas continuar con la misma apuesta pulse 2.\nSi deseas volver al menu pulse 3\n\n"))
    if respuesta == 1:
        coger_datos(correo_user)
    elif respuesta == 2:
        if apuesta <= dinero:
            combinacion()
        else:
            print("\nNo te queda tanto dinero")
            pregunta_final()
    elif respuesta == 3:
        ruta = os.path.join("src", "Menu.py")
        subprocess.run(["python", ruta, correo_user])
    else:
        quit()

coger_datos(correo_user)