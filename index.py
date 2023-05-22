import os
import subprocess

eleccion = ""

os.system("cls")

print("\033[96m" + "-------------------------------\n BIENVENIDO AL CASINO DE VIMEN\n-------------------------------\n")

while eleccion != 1 or eleccion != 0:
    eleccion = int(input("Si ya tienes cuenta pulse 0 para iniciar sesion, si aun no tienes cuenta pulse 1 para registrarte.\n\n"))
    if eleccion == 0 or eleccion == 1:
        break

if eleccion == 0:
     ruta = os.path.join("Usuarios", "Inicio_Sesion.py")
     subprocess.run(["python", ruta])

elif eleccion == 1:
    ruta = os.path.join("Usuarios", "Registro.py")
    subprocess.run(["python", ruta])