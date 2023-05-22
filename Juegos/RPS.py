import random
import sys
import subprocess
import os
from decouple import config
import mysql.connector

if len(sys.argv) > 1:
    correo_user = sys.argv[1]

opciones = ["Piedra", "Papel", "Tijera"]

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
    global dinero, wins_RPS, partidas_RPS, dinero_RPS
    consulta_dinero = "SELECT dinero FROM usuarios WHERE correo = %s"
    cursor.execute(consulta_dinero, (correo_user,))
    dinero_ = cursor.fetchone(); dinero = dinero_[0]

    consulta_wins_rps =  "SELECT partidas_rps_wins FROM usuarios WHERE correo = %s"
    cursor.execute(consulta_wins_rps, (correo_user,))
    wins_RPS_ = cursor.fetchone(); wins_RPS = wins_RPS_[0]

    consulta_partidas_rps =  "SELECT partidas_rps_totales FROM usuarios WHERE correo = %s"
    cursor.execute(consulta_partidas_rps, (correo_user,))
    partidas_RPS_ = cursor.fetchone(); partidas_RPS = partidas_RPS_[0]

    consulta_dinero_rps =  "SELECT rps_dinero FROM usuarios WHERE correo = %s"
    cursor.execute(consulta_dinero_rps, (correo_user,))
    dinero_RPS_ = cursor.fetchone(); dinero_RPS = dinero_RPS_[0]
    eleccion_player()

def eleccion_player():
    global apuesta, eleccion_persona
    apuesta = int(input(f"\nTienes {dinero}€, ¿cuanto dinero deseas apostar? --> "))
    while apuesta > dinero:
        apuesta = int(input(f"Tienes {dinero}€, ¿cuanto dinero deseas apostar? --> "))
    eleccion_persona = int(input("\n\nSi quieres jugar piedra pulse 1.\nSi quieres jugar papel pulse 2.\nSi quieres jugar tijera pulse 3.\n\n"))
    while eleccion_persona != 1 and eleccion_persona != 2 and eleccion_persona != 3:
        eleccion_persona = int(input("\n\nEleccion no valida.\nSi quieres jugar piedra pulse 1.\nSi quieres jugar papel pulse 2.\nSi quieres jugar tijera pulse 3.\n\n"))
    eleccion_bot(eleccion_persona)

def eleccion_bot(eleccion_persona):
    global eleccion_npc, resultado
    eleccion_npc = random.choice(opciones)

    if eleccion_npc == "Piedra":
        if eleccion_persona == 1:
            resultado = "empate"
            print(f"\nHe sacado {eleccion_npc}, empate!\n")
        elif eleccion_persona == 2:
            resultado = "win"
            print(f"\nHe sacado {eleccion_npc}, has ganado!\n")
        else:
            resultado = "derrota"
            print(f"\nHe sacado {eleccion_npc}, has perdido!\n")

    elif eleccion_npc == "Papel":
        if eleccion_persona == 1:
            resultado = "derrota"
            print(f"\nHe sacado {eleccion_npc}, has perdido!\n")
        elif eleccion_persona == 2:
            resultado = "empate"
            print(f"\nHe sacado {eleccion_npc}, empate!\n")
        else:
            resultado = "win"
            print(f"\nHe sacado {eleccion_npc}, has ganado!\n")

    elif eleccion_npc == "Tijera":
        if eleccion_persona == 1:
            resultado = "win"
            print(f"\nHe sacado {eleccion_npc}, has ganado!\n")
        elif eleccion_persona == 2:
            resultado = "derrota"
            print(f"\nHe sacado {eleccion_npc}, has perdido!\n")
        else:
            resultado = "empate"
            print(f"\nHe sacado {eleccion_npc}, empate!\n")
    
    calcular_premio()

def calcular_premio():
    global premio
    if resultado == "win":
        premio = apuesta * 1.5
    elif resultado == "empate":
        premio = apuesta
    else:
        premio = 0
    
    dar_premio()

def dar_premio():
    global dinero,dinero_RPS,partidas_RPS,wins_RPS
    ganancia = premio - apuesta
    dinero += ganancia
    dinero_RPS += apuesta
    partidas_RPS += 1
    if resultado == "win":
        wins_RPS += 1
        print(f"Has ganado {premio}€\n")
    guardar_datos(dinero,dinero_RPS,partidas_RPS,wins_RPS)

def guardar_datos(dinero,dinero_RPS,partidas_RPS,wins_RPS):  
    guardar_dinero = "UPDATE usuarios SET dinero = %s WHERE correo = %s"
    cursor.execute(guardar_dinero, (dinero, correo_user))

    guardar_dinero_RPS = "UPDATE usuarios SET rps_dinero = %s WHERE correo = %s"
    cursor.execute(guardar_dinero_RPS, (dinero_RPS, correo_user))

    guardar_partidas_RPS = "UPDATE usuarios SET partidas_rps_totales = %s WHERE correo = %s"
    cursor.execute(guardar_partidas_RPS, (partidas_RPS, correo_user))

    guardar_wins_RPS = "UPDATE usuarios SET partidas_rps_wins = %s WHERE correo = %s"
    cursor.execute(guardar_wins_RPS, (wins_RPS, correo_user))

    conexion.commit()
    pregunta_final()

def pregunta_final():
    respuesta = int(input(f"Tienes {dinero}€.\nSi deseas salir pulse 0.\nSi deseas cambiar la apuesta pulse 1.\nSi deseas continuar con la misma apuesta pulse 2.\nSi deseas volver al menu pulse 3\n\n"))
    if respuesta == 1:
        coger_datos(correo_user)
    elif respuesta == 2:
        if apuesta <= dinero:
            eleccion_bot(eleccion_persona)
        else:
            print("\nNo te queda tanto dinero")
            pregunta_final()
    elif respuesta == 3:
        ruta = os.path.join("src", "Menu.py")
        subprocess.run(["python", ruta, correo_user])
    else:
        quit()

coger_datos(correo_user)