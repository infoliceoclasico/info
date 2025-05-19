import csv
import requests
from datetime import datetime

# URL del Apps Script (reemplazá con tu propia URL activa)
URL_SCRIPT = "https://script.google.com/macros/s/AKfycbxro0cHBpt4M42yDk0SYvBRvUYwyYeaBmy0yxKxLc7ht4faCEnv498xsDHOkxP2lpcI/exec"

# Punto de acceso (puerta)
PUNTO_ACCESO = "Puerta Principal"

# Cargar base de datos de alumnos desde archivo CSV
def cargar_alumnos():
    alumnos = {}
    with open("alumnos.csv", mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo, delimiter=";")
        for fila in lector:
            alumnos[fila["CODIGO"]] = fila
    return alumnos

# Registrar asistencia y mostrar mensajes claros
def registrar_asistencia(alumno):
    datos = {
        "codigo": alumno["CODIGO"],
        "nombre": alumno["NOMBRE"],
        "grado": alumno["GRADO"],
        "jornada": alumno["JORNADA"],
        "punto": PUNTO_ACCESO
    }

    try:
        respuesta = requests.post(URL_SCRIPT, data=datos)
        texto = respuesta.text.strip()

        if texto == "OK":
            print(f"✅ Asistencia registrada para {alumno['NOMBRE']} – {alumno['GRADO']} ({alumno['JORNADA']})")
        elif texto == "YA_REGISTRADO":
            print(f"⚠️ Este alumno ya registró asistencia hoy: {alumno['NOMBRE']} – {alumno['GRADO']}")
        else:
            print(f"⚠️ Respuesta inesperada del servidor: {texto}")
    except Exception as e:
        print(f"❌ Error al conectar con el servidor: {e}")

# Función principal
def main():
    alumnos = cargar_alumnos()
    while True:
        codigo = input("Ingrese su código (o escriba 'salir'): ").strip()
        if codigo.lower() == "salir":
            break
        alumno = alumnos.get(codigo)
        if alumno:
            registrar_asistencia(alumno)
        else:
            print("❌ Código no encontrado. Intente nuevamente.")

# Ejecutar programa
if __name__ == "__main__":
    main()
