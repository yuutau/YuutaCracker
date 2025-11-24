import os
import subprocess
import sys
import time
import json
import logging
import requests
from shutil import which
from datetime import datetime
import signal 
import ctypes
import hashlib

# ct ppl on top
# dependencias papu
try:
    from pystyle import Anime, Center, Colorate, Colors
except ImportError:
    print("Instalando dependencias necesarias (pystyle)...")
    os.system("pip install pystyle")
    from pystyle import Anime, Center, Colorate, Colors

ascii_art = r'''
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠻⠿⢿⣿⣿⣿⣿⣿⣶⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠻⠿⢿⣿⣿⣿⣿⣿⣶⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⣿⣿⣿⣿⣿⣿⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣙⢿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠻⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⡟⠹⠿⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡿⠋⡭⢿⣿⣷⣤⣤⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⡇⢸⡇⢸⣿⣿⣿⠟⠁⢀⣬⢽⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣧⣈⣛⣿⣿⣿⡇⠀⠀⣾⠁⢀⢻⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣧⣄⣀⠙⠷⢋⣼⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
                    ⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
                    ⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁
                    ⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀
                    ⠸⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀
                    ⠀⢹⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀
                    ⠀⠀⠹⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀
                    ⠀⠀⠀⠙⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
                   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀                   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠛⠛⠛⠛⠛⠛⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
/$$     /$$                     /$$
|  $$   /$$/                    | $$
\  $$ /$$//$$   /$$ /$$   /$$ /$$$$$$    /$$$$$$          /$$  /$$  /$$  /$$$$$$   /$$$$$$   /$$$$$$$  /$$$$$$
 \  $$$$/| $$  | $$| $$  | $$|_  $$_/   |____  $$ /$$$$$$| $$ | $$ | $$ /$$__  $$ |____  $$ /$$_____/ /$$__  $$
  \  $$/ | $$  | $$| $$  | $$  | $$      /$$$$$$$|______/| $$ | $$ | $$| $$  \ $$  /$$$$$$$| $$      | $$  \__/
   | $$  | $$  | $$| $$  | $$  | $$ /$$ /$$__  $$        | $$ | $$ | $$| $$  | $$ /$$__  $$| $$      | $$      
   | $$  |  $$$$$$/|  $$$$$$/  |  $$$$/|  $$$$$$$        |  $$$$$/$$$$/| $$$$$$$/|  $$$$$$$|  $$$$$$$| $$      
   |__/   \______/  \______/    \___/   \_______/         \_____/\___/ | $$____/  \_______/ \_______/|__/      
                                                                       | $$                                    
                                                                       | $$                                    
                                                                       |__/         
                                       || Press Enter to start ||                                                           
                                    
'''

ascii_calavera_verde = r'''
⠀⠀⠀⠀⠀⣶⡆⠀⠀⠀⢀⣴⢦⠀⠀⠀⠀⣖⡶⠀⠀⠀⠀⡏⡧⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢹⣷⡀⠀⠀⢀⣿⣧⡀⠀⠀⢠⣾⣧⠀⠀⠀⣠⣾⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⣿⣿⣦⡀⣼⣿⣿⣷⡀⢠⣿⣿⣿⡆⢀⣾⣿⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠋⠙⢿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠠⣤⣉⣙⠛⠛⠛⠛⠿⠿⠁⣴⣦⡈⠻⠛⠛⠛⢛⣉⣁⡤⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠉⠛⠻⠿⠶⣶⣆⠈⢿⡿⠃⣠⣶⡿⠿⠟⠛⠉⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣿⣿⣶⣶⣤⣤⣤⣤⡀⢁⣠⣤⣤⣤⣶⣶⣿⣿⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣸⣿⡏⠉⠙⠛⠿⢿⣿⣿⣾⣿⡿⠿⠛⠋⠉⠹⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠻⢿⣧⣀⠀⠀⣀⣀⣼⡿⣿⣯⣀⣀⠀⠀⣀⣼⡿⠗⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⠁⠘⣿⣿⣿⣿⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣇⣀⣀⣹⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⠿⣿⡿⢿⣿⠿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡇⢀⣿⡇⢸⣿⡀⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
     /\_/\  
    ( o.o ) 
     > ^ <
  GitHub: yuutau   t.me/valuado
'''

class Colores:
    rojo = '\033[91m'
    verde = '\033[92m'
    amarillo = '\033[93m'
    azul = '\033[94m'
    cyan = '\033[96m'
    reset = '\033[0m'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(filename=os.path.join(BASE_DIR, "yuutacracker.log"), level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

configuracion = {
    "modo_sigiloso": True,
    "dispositivo_preferido": None,
    "ruta_hashcat": "",
}

configuracion.update({
    "idioma": "es", 
    "notificaciones_discord": False, 
    "webhook_discord": "", 
    "usar_multiples_gpus": False, 
    "optimizar_automaticamente": True, 
    "sesion_actual": None, 
})

traducciones = {
    "es": {
        "menu_opciones": [
            "[1] Mostrar algoritmos soportados",
            "[2] Ataque por fuerza bruta",
            "[3] Ataque por diccionario",
            "[4] Ataque combinado",
            "[5] Ataque híbrido",
            "[6] Mostrar historial",
            "[7] Buscar hash en base de datos",
            "[8] Cambiar idioma",
            "[9] Ejecutar benchmark",
            "[10] Salir"
        ],
        "selecciona_opcion": "Selecciona una opcion: ",
        "hashcat_iniciando": "[INFO] Hashcat iniciando...",
        "clave_encontrada": "[✓] Clave encontrada: ",
        "ataque_finalizado": "[✓] Ataque finalizado.",
        "error_hashcat": "[!] Error en Hashcat:",
        "error_inesperado": "[!] Error inesperado:",
        "idioma_cambiado": "[INFO] Idioma cambiado a: ",
        "formato_hash": "Selecciona el formato de hash (ej. 22000): ",
        "restaurar_sesion": "Nombre de la sesion a restaurar: ",
        "gpu_multiples": "¿Usar multiples GPUs? (s/n): ",
        "discord_notificaciones": "¿Activar notificaciones por Discord? (s/n): ",
        "webhook_discord": "Introduce la URL del webhook de Discord: ",
        "benchmark_iniciando": "[INFO] Ejecutando benchmark de Hashcat...",
        "benchmark_finalizado": "[✓] Benchmark finalizado.",
        "verificando_actualizaciones": "[INFO] Verificando actualizaciones...",
        "ultima_version": "[INFO] Última versión disponible: ",
        "actualizacion_disponible": "[INFO] Si deseas actualizar, descarga la última versión desde el repositorio de GitHub.",
        "error_actualizaciones": "[!] No se pudo verificar actualizaciones. Intenta más tarde.",
    },
    "en": {
        "menu_opciones": [
            "[1] Show supported algorithms",
            "[2] Brute-force attack",
            "[3] Dictionary attack",
            "[4] Combined attack",
            "[5] Hybrid attack",
            "[6] Show history",
            "[7] Search hash in database",
            "[8] Change language",
            "[9] Run benchmark",
            "[10] Exit"
        ],
        "selecciona_opcion": "Select an option: ",
        "hashcat_iniciando": "[INFO] Hashcat starting...",
        "clave_encontrada": "[✓] Key found: ",
        "ataque_finalizado": "[✓] Attack finished.",
        "error_hashcat": "[!] Error in Hashcat:",
        "error_inesperado": "[!] Unexpected error:",
        "idioma_cambiado": "[INFO] Language changed to: ",
        "formato_hash": "Select hash format (e.g., 22000): ",
        "restaurar_sesion": "Session name to restore: ",
        "gpu_multiples": "Use multiple GPUs? (y/n): ",
        "discord_notificaciones": "Enable Discord notifications? (y/n): ",
        "webhook_discord": "Enter the Discord webhook URL: ",
        "benchmark_iniciando": "[INFO] Running Hashcat benchmark...",
        "benchmark_finalizado": "[✓] Benchmark completed.",
        "verificando_actualizaciones": "[INFO] Checking for updates...",
        "ultima_version": "[INFO] Latest version available: ",
        "actualizacion_disponible": "[INFO] If you want to update, download the latest version from the GitHub repository.",
        "error_actualizaciones": "[!] Could not check for updates. Try again later.",
    }
}

ALGORITMOS_HASH = {
    "0": "MD5",
    "100": "SHA1",
    "1400": "SHA256",
    "1700": "SHA512",
    "22000": "WPA/WPA2",
}

def t(clave):
    return traducciones[configuracion["idioma"]].get(clave, clave)

def validar_entrada_hashcat():
    if not configuracion["ruta_hashcat"]:
        print(Colores.rojo + "[!] Hashcat no esta configurado correctamente." + Colores.reset)
        return False
    return True

def restaurar_sesion():
    sesion = input(t("restaurar_sesion")).strip()
    if sesion:
        configuracion["sesion_actual"] = sesion
        print(Colores.verde + f"[INFO] Sesion restaurada: {sesion}" + Colores.reset)

def enviar_notificacion_discord(mensaje):
    if configuracion["notificaciones_discord"] and configuracion["webhook_discord"]:
        try:
            import requests
            data = {"content": mensaje}
            requests.post(configuracion["webhook_discord"], json=data)
            print(Colores.verde + "[INFO] Notificacion enviada a Discord." + Colores.reset)
        except Exception as e:
            print(Colores.rojo + f"[!] Error al enviar notificacion a Discord: {e}" + Colores.reset)
            logging.error(f"Error al enviar notificacion a Discord: {e}")

def optimizar_parametros():
    try:
        hashcat = configuracion.get("ruta_hashcat")
        if not hashcat:
            return None

        proceso = subprocess.Popen(
            [hashcat, "-I"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        salida = proceso.communicate()[0]

        dispositivos = []

        for linea in salida.splitlines():
            if "Device #" in linea or "Backend" in linea:
                dispositivos.append(linea.strip())

        return dispositivos

    except Exception as e:
        logging.error(f"Error en optimización: {e}")
        return None


def configurar_multiples_gpus():
    respuesta = input(t("gpu_multiples")).strip().lower()
    configuracion["usar_multiples_gpus"] = respuesta == "s" if configuracion["idioma"] == "es" else respuesta == "y"

def cambiar_idioma():
    idioma = input("Idioma / Language (es/en): ").strip().lower()
    if idioma in ["es", "en"]:
        configuracion["idioma"] = idioma
        print(Colores.verde + t("idioma_cambiado") + idioma + Colores.reset)
    else:
        print(Colores.rojo + "Idioma no valido. Selecciona 'es' o 'en'." + Colores.reset)

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def mostrar_banner():
    Anime.Fade(Center.Center(ascii_art), Colors.red_to_blue, Colorate.Vertical, interval=0.035, enter=True)
    
def mostrar_calavera_verde():
    print(Colorate.Vertical(Colors.purple_to_blue, Center.Center(ascii_calavera_verde)))

def buscar_hashcat():
    hashcat_path = which("hashcat")
    if hashcat_path and os.path.isfile(hashcat_path):
        return hashcat_path

    print("[INFO] Buscando hashcat.exe globalmente...")

    unidades = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(26):
        if bitmask & (1 << i):
            unidades.append(letras[i] + ":\\")

    for unidad in unidades:
        for root, dirs, files in os.walk(unidad, topdown=True):
            dirs[:] = [d for d in dirs if d.lower() not in ["windows", "programdata", "appdata", "recycle.bin"]]

            if "hashcat.exe" in files:
                ruta = os.path.join(root, "hashcat.exe")
                print(f"[INFO] Encontrado: {ruta}")
                return ruta

    manual = input("Ruta de hashcat.exe: ").strip().strip('"')
    if os.path.isfile(manual):
        return manual

    print("[!] No se encontró hashcat.exe en todo el sistema.")
    return None

def asegurar_directorio_hashcat(path_hashcat):
    carpeta = os.path.dirname(path_hashcat)
    os.chdir(carpeta)

def seleccionar_dispositivo(hashcat):
    try:
        print(Colores.cyan + "\nDispositivos disponibles:\n" + Colores.reset)
        resultado = subprocess.check_output([hashcat, "-I"], stderr=subprocess.STDOUT, text=True)
        print(resultado)
        dispositivo = input("ID de dispositivo a usar (ej. 1): ").strip()
        configuracion["dispositivo_preferido"] = dispositivo
    except subprocess.CalledProcessError as e:
        print(Colores.rojo + "[!] No se pudo detectar dispositivos:\n" + Colores.reset + e.output)

def generar_mascara_personalizada():
    """
    Genera una máscara simple basada en la longitud y tipo de caracteres.
    Devuelve la máscara (ej. '?l?l?d?d') o None si el usuario cancela.
    """
    try:
        longitud = input("Longitud (enter para cancelar): ").strip()
        if longitud == "":
            return None
        longitud = int(longitud)
    except ValueError:
        print(Colores.rojo + "Longitud invalida." + Colores.reset)
        return None

    print("Tipo de caracteres:")
    print("[1] Minusculas")
    print("[2] Mayusculas")
    print("[3] Numeros")
    print("[4] Alfanumerico (mix)")
    opcion = input("Selecciona tipo: ").strip()

    if opcion == "1":
        plantilla = "?l"
    elif opcion == "2":
        plantilla = "?u"
    elif opcion == "3":
        plantilla = "?d"
    elif opcion == "4":
        plantilla = "?l?u?d"
    else:
        print(Colores.rojo + "Opcion invalida." + Colores.reset)
        return None

    if len(plantilla) > 2 and plantilla.count("?") > 1:
        mascara = "".join(plantilla.split("?")[1:][i % len(plantilla.split("?")[1:])] for i in range(longitud))
        if not mascara:
            mascara = "?l" * longitud
    else:
        mascara = plantilla * longitud

    print(Colores.verde + f"[INFO] Mascara generada: {mascara}" + Colores.reset)
    return mascara

def mostrar_estado_diccionario(start_time, total_lines, current_line, keys_per_sec):
    transcurrido = int(time.time() - start_time)
    restante = int((total_lines - current_line) / keys_per_sec) if keys_per_sec > 0 else 0

    def formato(segundos):
        mins, secs = divmod(segundos, 60)
        hours, mins = divmod(mins, 60)
        return f"{hours:02}:{mins:02}:{secs:02}"

    print(Colores.cyan + f"\n[INFO] Claves por segundo: {int(keys_per_sec):,} H/s" + Colores.reset)
    print(f"[INFO] Progreso: {current_line:,} / {total_lines:,}")
    print(f"[INFO] Tiempo transcurrido: {formato(transcurrido)}")
    print(f"[INFO] Estimado restante: {formato(restante)}")
    print(Colores.amarillo + "\nTeclas utiles: [q] salir  [p] pausar  [r] reanudar\n" + Colores.reset)

def validar_archivo(ruta):
    if not os.path.isfile(ruta):
        print(Colores.rojo + f"[!] Archivo no encontrado: {ruta}" + Colores.reset)
        return False
    return True

def guardar_clave_en_archivo(clave):
    try:
        ruta_archivo = os.path.join(BASE_DIR, "clave_encontrada.txt")
        with open(ruta_archivo, "a") as file:
            file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {clave}\n")
        print(Colores.verde + f"\n[✓] Clave guardada en {ruta_archivo}" + Colores.reset)
        logging.info(f"Clave guardada: {clave}")
    except Exception as e:
        print(Colores.rojo + f"[!] Error al guardar la clave: {e}" + Colores.reset)
        logging.error(f"Error al guardar la clave: {e}")

def configurar_notificaciones_discord():
    respuesta = input(t("discord_notificaciones")).strip().lower()
    configuracion["notificaciones_discord"] = respuesta == ("s" if configuracion["idioma"] == "es" else "y")
    if configuracion["notificaciones_discord"]:
        webhook = input(t("webhook_discord")).strip()
        configuracion["webhook_discord"] = webhook
        print(Colores.verde + t("notificaciones_activadas") + Colores.reset)
    else:
        configuracion["webhook_discord"] = ""
        print(Colores.amarillo + t("notificaciones_desactivadas") + Colores.reset)

def lanzar_hashcat(archivo, mascara, modo, diccionario=None, reglas=None, diccionarios=None, formato_hash="22000"):
    try:
        tiempo_inicio = datetime.now() 
        hashcat = configuracion["ruta_hashcat"]
        if not hashcat:
            print(Colores.rojo + "[!] Ruta de Hashcat no definida. Asegurate de que Hashcat este instalado y configurado correctamente." + Colores.reset)
            return
        if not validar_archivo(archivo):
            return
        if modo == "diccionario" and not validar_archivo(diccionario):
            return

        args = [hashcat, "-m", formato_hash, "--optimized-kernel-enable", "--kernel-accel=64", "--kernel-loops=256", "--hwmon-temp-abort=90", "--force"]
        args += ["-a", "3" if modo == "bruteforce" else "0"]
        args.append(archivo)
        args.append(mascara if modo == "bruteforce" else diccionario)

        if reglas:
            args += ["-r", reglas]
        if diccionarios:
            args += diccionarios

        if configuracion["dispositivo_preferido"]:
            args += ["--backend-devices", configuracion["dispositivo_preferido"]]
        args += ["--status", "--status-json", "--session", "yuuta-session", "--logfile-disable", "--potfile-disable"]
        if configuracion["modo_sigiloso"]:
            args.append("--quiet")

        print(Colores.cyan + "[INFO] Hashcat iniciando...\n" + Colores.reset)
        logging.info("Hashcat iniciado con argumentos: " + " ".join(args))

        asegurar_directorio_hashcat(hashcat)
        proceso = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        start_time = time.time()

        fallo = False 

        while proceso.poll() is None:
            output = proceso.stdout.readline().strip()
            if output:
                try:
                    data = json.loads(output)
                    mostrar_estado_hashcat(data, start_time)
                    if 'password' in data:
                        clave = data['password']
                        print(Colores.verde + f"\n[✓] Clave encontrada: {clave}" + Colores.reset)
                        guardar_clave_en_archivo(clave)
                        enviar_notificacion_discord(f"Clave encontrada: {clave}")
                        enviar_notificacion_telegram(f"Clave encontrada: {clave}")
                        generar_reporte_detallado(modo, archivo, clave, tiempo_inicio, datetime.now())
                        proceso.terminate()
                        break
                except json.JSONDecodeError:
                    if "error" in output.lower():
                        fallo = True
                    continue

        proceso.wait()

        resultado = "exito"
        if fallo or proceso.returncode != 0:
            resultado = "fallo"

        try:
            guardar_en_historial(modo, archivo, resultado)
        except Exception as e:
            logging.error("Error guardando historial: %s", e)

        try:
            if configuracion.get("webhook_discord") or configuracion.get("telegram_token"):
                enviar_notificacion_avanzada(
                    f"Ataque terminado ({resultado}). Archivo: {archivo}"
                )
        except Exception as e:
            logging.error("Error enviando notificación: %s", e)
        # ---------------------------------------------------------

        print(Colores.verde + "\n[✓] Ataque finalizado.\n" + Colores.reset)
        logging.info("Ataque finalizado.")
        enviar_notificacion_discord("Ataque finalizado.")
        enviar_notificacion_telegram("Ataque finalizado. Clave no encontrada.")
        generar_reporte_detallado(modo, archivo, "No encontrada", tiempo_inicio, datetime.now())
        time.sleep(1)

    except Exception as e:
        print(Colores.rojo + f"[!] Error inesperado: {e}" + Colores.reset)
        logging.error(f"Error inesperado: {e}")


def lanzar_hashcat_combinado(archivo, diccionario1, diccionario2, reglas=None, diccionarios=None, formato_hash="22000"):
    try:
        tiempo_inicio = datetime.now()
        hashcat = configuracion["ruta_hashcat"]
        if not hashcat:
            print("Ruta de Hashcat no definida.")
            return
        if not validar_archivo(archivo) or not validar_archivo(diccionario1) or not validar_archivo(diccionario2):
            return

        args = [
            hashcat, "-m", formato_hash, "-a", "1", archivo, diccionario1, diccionario2,
            "--optimized-kernel-enable", "--kernel-accel=64", "--kernel-loops=256",
            "--hwmon-temp-abort=90", "--force", "--status", "--status-json",
            "--session", "yuuta-session", "--logfile-disable", "--potfile-disable"
        ]

        if reglas:
            args += ["-r", reglas]
        if diccionarios:
            args += diccionarios

        if configuracion["dispositivo_preferido"]:
            args += ["--backend-devices", configuracion["dispositivo_preferido"]]
        if configuracion["modo_sigiloso"]:
            args.append("--quiet")

        asegurar_directorio_hashcat(hashcat)
        proceso = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        print(Colores.cyan + "[INFO] Hashcat iniciando en modo combinado...\n" + Colores.reset)
        logging.info("Hashcat iniciado en modo combinado con argumentos: " + " ".join(args))

        fallo = False

        while proceso.poll() is None:
            output = proceso.stdout.readline().strip()
            if output:
                try:
                    data = json.loads(output)
                    estado = mostrar_estado_hashcat(data)
                    if estado == "error":
                        fallo = True

                    if 'password' in data:
                        clave = data['password']
                        print(Colores.verde + f"\n[✓] Clave encontrada: {clave}" + Colores.reset)
                        guardar_clave_en_archivo(clave)
                        enviar_notificacion_discord(f"Clave encontrada: {clave}")
                        enviar_notificacion_telegram(f"Clave encontrada: {clave}")
                        generar_reporte_detallado("combinado", archivo, clave, tiempo_inicio, datetime.now())
                        proceso.terminate()
                        break

                except json.JSONDecodeError:
                    if "error" in output.lower():
                        fallo = True
                    pass

        proceso.wait()

        resultado = "exito"
        if fallo or proceso.returncode != 0:
            resultado = "fallo"

        try:
            guardar_en_historial("combinado", archivo, resultado)
        except Exception as e:
            logging.error("Error guardando historial: %s", e)

        try:
            if configuracion.get("webhook_discord") or configuracion.get("telegram_token"):
                enviar_notificacion_avanzada(
                    f"Ataque combinado terminado ({resultado}). Archivo: {archivo}"
                )
        except Exception as e:
            logging.error("Error enviando notificación: %s", e)

        print(Colores.verde + "\n[✓] Ataque combinado finalizado.\n" + Colores.reset)
        logging.info("Ataque combinado finalizado.")
        enviar_notificacion_discord("Ataque combinado finalizado.")
        enviar_notificacion_telegram("Ataque combinado finalizado. Clave no encontrada.")
        generar_reporte_detallado("combinado", archivo, "No encontrada", tiempo_inicio, datetime.now())
        time.sleep(1)

    except subprocess.CalledProcessError as e:
        print(Colores.rojo + "[!] Error en hashcat:\n" + Colores.reset + str(e))
        logging.error(f"Error en hashcat: {e}")
    except Exception as e:
        print(Colores.rojo + f"[!] Error inesperado: {e}" + Colores.reset)
        logging.error(f"Error inesperado: {e}")


def mostrar_estado_hashcat(data, start_time=None):
    """
    Interpreta el JSON de Hashcat. Devuelve:
    - "found" si Hashcat ha encontrado una clave
    - "error" si detecta un error
    - None para continuar normalmente
    """
    try:
        if not isinstance(data, dict):
            return None

        if "error" in str(data).lower():
            print(Colores.rojo + "[!] Hashcat reportó un error." + Colores.reset)
            return "error"

        if "password" in data:
            return "found"

        if "devices" in data:
            speed_total = 0
            for dev in data["devices"]:
                try:
                    speed_total += int(dev.get("speed", 0))
                except:
                    pass

            print(Colores.cyan + f"[INFO] Claves por segundo: {speed_total:,} H/s" + Colores.reset)

        if "progress" in data and isinstance(data["progress"], list) and len(data["progress"]) == 2:
            prog, total = data["progress"]
            try:
                pct = (prog / total) * 100
                print(Colores.amarillo + f"[INFO] Progreso: {pct:.2f}% ({prog}/{total})" + Colores.reset)
            except:
                pass

        if start_time is not None:
            elapsed = time.time() - start_time
            print(Colores.cyan + f"[INFO] Tiempo: {elapsed:.1f}s" + Colores.reset)

        return None

    except Exception as e:
        print(Colores.rojo + f"[!] Error en mostrar_estado_hashcat: {e}" + Colores.reset)
        return "error"

def guardar_en_historial(tipo_ataque, archivo, resultado):
    try:
        ruta_historial = os.path.join(BASE_DIR, "historial.txt")
        with open(ruta_historial, "a", encoding="utf-8") as file:
            file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Tipo: {tipo_ataque}, Archivo: {archivo}, Resultado: {resultado}\n")
        logging.info("Historial actualizado: %s %s %s", tipo_ataque, archivo, resultado)
    except Exception as e:
        logging.error("Error guardando historial: %s", e, exc_info=True)

def mostrar_historial():
    try:
        ruta_historial = os.path.join(BASE_DIR, "historial.txt")
        with open(ruta_historial, "r") as file:
            print(Colores.cyan + "\n[INFO] Historial de ataques:\n" + Colores.reset)
            print(file.read())
    except FileNotFoundError:
        print(Colores.amarillo + "[INFO] No hay historial disponible." + Colores.reset)

def seleccionar_diccionarios():
    diccionarios = []
    print(Colores.cyan + "[INFO] Selecciona los diccionarios (escribe 'done' para terminar):" + Colores.reset)
    while True:
        diccionario = input("Diccionario: ").strip()
        if diccionario.lower() == "done":
            break
        if validar_archivo(diccionario):
            diccionarios.append(diccionario)
        else:
            print(Colores.rojo + "[!] Diccionario no valido." + Colores.reset)
    return diccionarios

def buscar_en_base_de_datos(hash_input):
    """
    Espera una contraseña en texto u hash. Si parece ser un hash SHA1 (40 hex), usa HIBP range API.
    Si recibe texto plano, calcula su SHA1 y lo busca.
    """
    try:
        posible = hash_input.strip()
        if len(posible) != 40 or not all(c in "0123456789abcdefABCDEF" for c in posible):
            sha1 = hashlib.sha1(posible.encode("utf-8")).hexdigest().upper()
        else:
            sha1 = posible.upper()

        prefix = sha1[:5]
        suffix = sha1[5:]

        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        import requests
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            print(Colores.amarillo + "[INFO] No se pudo consultar la base de datos HIBP." + Colores.reset)
            return False

        lines = resp.text.splitlines()
        for line in lines:
            parts = line.split(':')
            if len(parts) >= 2 and parts[0].strip().upper() == suffix:
                count = parts[1].strip()
                print(Colores.rojo + f"[!] Hash encontrado en HIBP (veces): {count}" + Colores.reset)
                return True

        print(Colores.verde + "[INFO] Hash no encontrado en HIBP." + Colores.reset)
        return False
    except Exception as e:
        print(Colores.rojo + f"[!] Error al buscar en base de datos: {e}" + Colores.reset)
        return False

def seleccionar_reglas():
    reglas = input("Archivo de reglas (.rule): ").strip()
    if validar_archivo(reglas):
        return reglas
    else:
        print(Colores.rojo + "[!] Archivo de reglas no valido." + Colores.reset)
        return None

def enviar_notificacion_avanzada(mensaje):
    """
    Envía notificaciones por Telegram y/o Discord Webhook.
    - Usa configuracion["telegram_token"] y configuracion["telegram_chatid"]
    - Usa configuracion["webhook_discord"]
    Retorna True si al menos un método se envió correctamente.
    """

    exito = False

    try:
        token = configuracion.get("telegram_token")
        chat_id = configuracion.get("telegram_chatid")

        if token and chat_id:
            import requests
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = {"chat_id": chat_id, "text": mensaje}
            r = requests.post(url, data=data, timeout=8)

            if r.status_code == 200:
                exito = True
            else:
                print(Colores.amarillo + f"[!] Telegram devolvió {r.status_code}: {r.text}" + Colores.reset)

    except Exception as e:
        print(Colores.rojo + f"[!] Error enviando Telegram: {e}" + Colores.reset)
        logging.error("Error Telegram: %s", e)

    try:
        webhook = configuracion.get("webhook_discord")
        if webhook:
            import requests
            payload = {"content": mensaje}
            r = requests.post(webhook, json=payload, timeout=8)

            if r.status_code in (200, 204):
                exito = True
            else:
                print(Colores.amarillo + f"[!] Discord devolvió {r.status_code}: {r.text}" + Colores.reset)

    except Exception as e:
        print(Colores.rojo + f"[!] Error enviando Discord: {e}" + Colores.reset)
        logging.error("Error Discord: %s", e)

    return exito
def lanzar_ataque_hibrido(archivo, diccionario, mascara, reglas=None, diccionarios=None, formato_hash="22000"):
    try:
        tiempo_inicio = datetime.now()
        hashcat = configuracion["ruta_hashcat"]
        if not hashcat:
            print(Colores.rojo + "[!] Ruta de Hashcat no definida." + Colores.reset)
            return
        if not validar_archivo(archivo) or not validar_archivo(diccionario):
            return

        args = [
            hashcat, "-m", formato_hash, "-a", "6", archivo, diccionario, mascara,
            "--optimized-kernel-enable", "--kernel-accel=64", "--kernel-loops=256",
            "--hwmon-temp-abort=90", "--force", "--status", "--status-json",
            "--session", "yuuta-session", "--logfile-disable", "--potfile-disable"
        ]

        if reglas:
            args += ["-r", reglas]
        if diccionarios:
            args += diccionarios

        if configuracion["dispositivo_preferido"]:
            args += ["--backend-devices", configuracion["dispositivo_preferido"]]
        if configuracion["modo_sigiloso"]:
            args.append("--quiet")

        print(Colores.cyan + "[INFO] Hashcat iniciando en modo hibrido...\n" + Colores.reset)
        logging.info("Hashcat iniciado en modo hibrido con argumentos: " + " ".join(args))

        asegurar_directorio_hashcat(hashcat)
        proceso = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        fallo = False

        while proceso.poll() is None:
            output = proceso.stdout.readline().strip()
            if not output:
                continue

            try:
                data = json.loads(output)
                estado = mostrar_estado_hashcat(data)

                if estado == "error":
                    fallo = True

                if 'password' in data:
                    clave = data['password']
                    print(Colores.verde + f"\n[✓] Clave encontrada: {clave}" + Colores.reset)
                    guardar_clave_en_archivo(clave)
                    enviar_notificacion_discord(f"Clave encontrada: {clave}")
                    enviar_notificacion_telegram(f"Clave encontrada: {clave}")
                    generar_reporte_detallado("hibrido", archivo, clave, tiempo_inicio, datetime.now())
                    proceso.terminate()
                    break

            except json.JSONDecodeError:
                if "error" in output.lower() or "no such file" in output.lower():
                    fallo = True
                print(output)

        proceso.wait()

        resultado = "exito"
        if fallo or proceso.returncode != 0:
            resultado = "fallo"

        try:
            guardar_en_historial("hibrido", archivo, resultado)
        except Exception as e:
            logging.error("Error guardando historial: %s", e)

        try:
            if configuracion.get("webhook_discord") or configuracion.get("telegram_token"):
                enviar_notificacion_avanzada(
                    f"Ataque hibrido terminado ({resultado}). Archivo: {archivo}"
                )
        except Exception as e:
            logging.error("Error enviando notificación: %s", e)

        print(Colores.verde + "\n[✓] Ataque hibrido finalizado.\n" + Colores.reset)
        logging.info("Ataque hibrido finalizado.")
        enviar_notificacion_discord("Ataque hibrido finalizado.")
        enviar_notificacion_telegram("Ataque hibrido finalizado. Clave no encontrada.")
        generar_reporte_detallado("hibrido", archivo, "No encontrada", tiempo_inicio, datetime.now())
        time.sleep(1)

    except Exception as e:
        print(Colores.rojo + f"[!] Error al iniciar el ataque hibrido: {e}" + Colores.reset)
        logging.error(f"Error en ataque hibrido: {e}")


# Validacion de dependencias
def validar_dependencias():
    try:
        import requests
        print(Colores.verde + "[INFO] Dependencias validadas correctamente." + Colores.reset)
    except ImportError:
        print(Colores.rojo + "[!] Falta instalar la dependencia 'requests'. Ejecuta 'pip install requests'." + Colores.reset)
        sys.exit(1)

def configurar_ataque(modo):
    print(Colores.cyan + t("configuraciones_adicionales") + Colores.reset)
    usar_reglas = input(t("usar_reglas")).strip().lower()
    reglas = seleccionar_reglas() if usar_reglas == ("s" if configuracion["idioma"] == "es" else "y") else None

    diccionarios = configurar_diccionarios_si_relevante(modo)

    usar_notificaciones_discord = input(t("activar_notificaciones")).strip().lower()
    if usar_notificaciones_discord == ("s" if configuracion["idioma"] == "es" else "y"):
        configurar_notificaciones_discord()

    usar_notificaciones_telegram = input(t("telegram_notificaciones")).strip().lower()
    if usar_notificaciones_telegram == ("s" if configuracion["idioma"] == "es" else "y"):
        configurar_notificaciones_telegram()

    return reglas, diccionarios


def mostrar_algoritmos():
    print(Colores.cyan + t("algoritmos_soportados") + Colores.reset)
    for codigo, nombre in ALGORITMOS_HASH.items():
        print(f"{codigo}: {nombre}")
    print()
    input(Colores.amarillo + t("presiona_enter") + Colores.reset)

def seleccionar_archivo():
    """
    Abre un diálogo para seleccionar un archivo.
    Devuelve ruta válida o None si el usuario cancela.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        archivo = filedialog.askopenfilename()

        root.destroy()

        if not archivo:
            return None

        return archivo.strip('"')

    except Exception as e:
        print(Colores.rojo + f"[!] Error al seleccionar archivo: {e}" + Colores.reset)
        return None

def validar_algoritmo_hash(hash_input):
    if hash_input not in ALGORITMOS_HASH:
        print(Colores.rojo + f"[!] Algoritmo de hash no soportado: {hash_input}" + Colores.reset)
        return False
    return True

def validar_archivo(ruta):
    if not ruta or not os.path.isfile(ruta):
        print(Colores.rojo + f"[!] Archivo no encontrado o invalido: {ruta}" + Colores.reset)
        return False
    return True

def configurar_diccionarios_si_relevante(modo):
    modo = modo.lower()
    if modo == "diccionario":
        print(Colores.cyan + "[INFO] Selecciona el diccionario para ataque por diccionario." + Colores.reset)
        dic = seleccionar_archivo()
        if not dic or not validar_archivo(dic):
            print(Colores.amarillo + "[INFO] Diccionario no seleccionado o inválido. Cancelando." + Colores.reset)
            return None
        return [dic]

    if modo == "combinado":
        print(Colores.cyan + "[INFO] Selecciona DOS diccionarios para ataque combinado." + Colores.reset)
        d1 = seleccionar_archivo()
        if not d1 or not validar_archivo(d1):
            print(Colores.amarillo + "[INFO] Primer diccionario no válido. Cancelando." + Colores.reset)
            return None
        d2 = seleccionar_archivo()
        if not d2 or not validar_archivo(d2):
            print(Colores.amarillo + "[INFO] Segundo diccionario no válido. Cancelando." + Colores.reset)
            return None
        return [d1, d2]

    if modo == "hibrido":
        print(Colores.cyan + "[INFO] Selecciona el diccionario (wordlist) para el modo híbrido." + Colores.reset)
        dic = seleccionar_archivo()
        if not dic or not validar_archivo(dic):
            print(Colores.amarillo + "[INFO] Diccionario no seleccionado o inválido. Cancelando." + Colores.reset)
            return None
        return [dic]

    return None


def configurar_notificaciones_telegram():
    respuesta = input(t("telegram_notificaciones")).strip().lower()
    configuracion["notificaciones_telegram"] = respuesta == ("s" if configuracion["idioma"] == "es" else "y")
    if configuracion["notificaciones_telegram"]:
        token = input(t("telegram_token")).strip()
        chat_id = input(t("telegram_chat_id")).strip()
        configuracion["telegram_token"] = token
        configuracion["telegram_chat_id"] = chat_id
        print(Colores.verde + t("notificaciones_activadas_telegram") + Colores.reset)
    else:
        configuracion["telegram_token"] = ""
        configuracion["telegram_chat_id"] = ""
        print(Colores.amarillo + t("notificaciones_desactivadas_telegram") + Colores.reset)

def enviar_notificacion_telegram(mensaje):
    if configuracion.get("notificaciones_telegram") and configuracion.get("telegram_token") and configuracion.get("telegram_chat_id"):
        try:
            url = f"https://api.telegram.org/bot{configuracion['telegram_token']}/sendMessage"
            data = {"chat_id": configuracion["telegram_chat_id"], "text": mensaje}
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print(Colores.verde + t("notificacion_enviada_telegram") + Colores.reset)
            else:
                print(Colores.rojo + t("error_notificacion_telegram") + Colores.reset)
        except Exception as e:
            print(Colores.rojo + f"[!] {t('error_notificacion_telegram')}: {e}" + Colores.reset)

def generar_reporte_detallado(tipo_ataque, archivo, resultado, tiempo_inicio, tiempo_fin):
    try:
        reporte = {
            "tipo_ataque": tipo_ataque,
            "archivo": archivo,
            "resultado": resultado,
            "tiempo_inicio": tiempo_inicio.strftime("%Y-%m-%d %H:%M:%S"),
            "tiempo_fin": tiempo_fin.strftime("%Y-%m-%d %H:%M:%S"),
            "duracion": str(tiempo_fin - tiempo_inicio),
        }
        nombre_reporte = f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        ruta_reporte = os.path.join(BASE_DIR, nombre_reporte)
        with open(ruta_reporte, "w") as file:
            json.dump(reporte, file, indent=4)
        print(Colores.verde + t("reporte_generado") + f": {ruta_reporte}" + Colores.reset)
    except Exception as e:
        print(Colores.rojo + f"[!] {t('error_generar_reporte')}: {e}" + Colores.reset)

traducciones["es"].update({
    "telegram_notificaciones": "¿Activar notificaciones por Telegram? (s/n): ",
    "telegram_token": "Introduce el token del bot de Telegram: ",
    "telegram_chat_id": "Introduce el ID del chat de Telegram: ",
    "notificaciones_activadas_telegram": "[INFO] Notificaciones de Telegram configuradas.",
    "notificaciones_desactivadas_telegram": "[INFO] Notificaciones de Telegram desactivadas.",
    "notificacion_enviada_telegram": "[INFO] Notificación enviada a Telegram.",
    "error_notificacion_telegram": "[!] Error al enviar notificación a Telegram.",
    "reporte_generado": "[INFO] Reporte generado",
    "error_generar_reporte": "[!] Error al generar el reporte.",
})

traducciones["en"].update({
    "telegram_notificaciones": "Enable Telegram notifications? (y/n): ",
    "telegram_token": "Enter the Telegram bot token: ",
    "telegram_chat_id": "Enter the Telegram chat ID: ",
    "notificaciones_activadas_telegram": "[INFO] Telegram notifications configured.",
    "notificaciones_desactivadas_telegram": "[INFO] Telegram notifications disabled.",
    "notificacion_enviada_telegram": "[INFO] Notification sent to Telegram.",
    "error_notificacion_telegram": "[!] Error sending notification to Telegram.",
    "reporte_generado": "[INFO] Report generated",
    "error_generar_reporte": "[!] Error generating the report.",
})

def manejar_ctrl_c(proceso):
    try:
        print(Colores.amarillo + "\n[!] Interrupción detectada. Finalizando Hashcat..." + Colores.reset)

        if proceso and proceso.poll() is None:
            proceso.terminate()
            time.sleep(0.5)
            try:
                proceso.kill()
            except:
                pass

        enviar_notificacion_avanzada("⚠ Ataque detenido manualmente (Ctrl+C).")

        print(Colores.rojo + "[X] Ataque cancelado." + Colores.reset)
        logging.info("Ataque cancelado por el usuario (Ctrl+C).")

    except Exception as e:
        print(Colores.rojo + f"[!] Error al manejar Ctrl + C: {e}" + Colores.reset)
        logging.error(f"Error manejando Ctrl+C: {e}")

def ejecutar_benchmark():
    """
    Ejecuta benchmark: se cambia al dir de hashcat, corre '-b', detecta errores y fuerza SIGINT al terminar.
    """
    try:
        hashcat = configuracion.get("ruta_hashcat")
        if not hashcat:
            print(Colores.rojo + "[!] Ruta de Hashcat no definida. Asegurate de que Hashcat este instalado y configurado correctamente." + Colores.reset)
            return

        carpeta = os.path.dirname(hashcat)
        if carpeta:
            asegurar_directorio_hashcat(hashcat)  # mantén la funcion existente que hace chdir
        print(Colores.cyan + "[INFO] Ejecutando benchmark de Hashcat...\n" + Colores.reset)

        proceso = subprocess.Popen([hashcat, "-b"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

        fallo = False
        for linea in proceso.stdout:
            estado = mostrar_estado_hashcat(linea)
            if estado == "error":
                fallo = True

        proceso.wait()

        if fallo or proceso.returncode != 0:
            print(Colores.rojo + "[X] Benchmark falló. No se encontró el entorno completo de Hashcat o ocurrió un error." + Colores.reset)
            logging.error("Benchmark falló. Returncode: %s", proceso.returncode)
            # breakpoint: avisar al usuario y forzar salida con Ctrl+C
            print(Colores.amarillo + "[!] Breakpoint: fallo en el benchmark. Saliendo..." + Colores.reset)
            os.kill(os.getpid(), signal.SIGINT)
        else:
            print(Colores.verde + "[✓] Benchmark finalizado exitosamente.\n" + Colores.reset)
            # forzar Ctrl+C como pediste
            os.kill(os.getpid(), signal.SIGINT)

    except Exception as e:
        print(Colores.rojo + f"[!] Error al ejecutar el benchmark: {e}" + Colores.reset)
        logging.error("Error en benchmark: %s", e, exc_info=True)



def menu():
    limpiar_pantalla()
    mostrar_banner()
    mostrar_calavera_verde()

    opciones = t("menu_opciones")
    for opcion in opciones:
        print(Colorate.Horizontal(Colors.red_to_yellow, opcion))

    print()
    opcion = input(t("selecciona_opcion")).strip()

    if opcion == "1":
        mostrar_algoritmos()
    elif opcion == "2":
        formato_hash = input(t("formato_hash")).strip()
        if not validar_algoritmo_hash(formato_hash):
            return

        archivo = seleccionar_archivo()
        if not validar_archivo(archivo):
            return

        mascara = generar_mascara_personalizada()
        reglas, diccionarios = configurar_ataque(modo="bruteforce")
        lanzar_hashcat(archivo, mascara, "bruteforce", reglas=reglas, diccionarios=diccionarios, formato_hash=formato_hash)
    elif opcion == "3":
        formato_hash = input(t("formato_hash")).strip()
        if not validar_algoritmo_hash(formato_hash):
            return

        archivo = seleccionar_archivo()
        if not validar_archivo(archivo):
            return

        diccionario = seleccionar_archivo()
        if not validar_archivo(diccionario):
            return

        reglas, diccionarios = configurar_ataque(modo="diccionario")
        if not diccionarios:
            return
        lanzar_hashcat(archivo, None, "diccionario", diccionario=diccionarios[0], reglas=reglas, diccionarios=None, formato_hash=formato_hash)

    elif opcion == "4":
        formato_hash = input(t("formato_hash")).strip()
        if not validar_algoritmo_hash(formato_hash):
            return

        archivo = seleccionar_archivo()
        if not validar_archivo(archivo):
            return

        diccionario1 = seleccionar_archivo()
        diccionario2 = seleccionar_archivo()
        if not validar_archivo(diccionario1) or not validar_archivo(diccionario2):
            return

        reglas, diccionarios = configurar_ataque(modo="combinado")
        lanzar_hashcat_combinado(archivo, diccionario1, diccionario2, reglas=reglas, diccionarios=diccionarios, formato_hash=formato_hash)
    elif opcion == "5":
        formato_hash = input(t("formato_hash")).strip()
        if not validar_algoritmo_hash(formato_hash):
            return

        archivo = seleccionar_archivo()
        if not validar_archivo(archivo):
            return

        diccionario = seleccionar_archivo()
        if not validar_archivo(diccionario):
            return

        mascara = input("Mascara: ").strip()
        reglas, diccionarios = configurar_ataque(modo="hibrido")
        lanzar_ataque_hibrido(archivo, diccionario, mascara, reglas=reglas, diccionarios=diccionarios, formato_hash=formato_hash)
    elif opcion == "6": 
        mostrar_historial()
    elif opcion == "7":  # Buscar hash en base de datos
        hash_input = input(t("introduce_hash")).strip()
        buscar_en_base_de_datos(hash_input)
    elif opcion == "8":  # Cambiar idioma
        cambiar_idioma()
    elif opcion == "9":  # Benchmark
        ejecutar_benchmark()
    elif opcion == "10":  # Salir
        print(t("saliendo"))
        logging.info("Programa finalizado por el usuario.")
        sys.exit(0)
    else:
        print(t("opcion_invalida"))
    time.sleep(1)

traducciones["es"].update({
    "introduce_hash": "Introduce el hash a buscar: ",
    "saliendo": "Saliendo...",
    "opcion_invalida": "Opcion invalida.",
})
traducciones["en"].update({
    "introduce_hash": "Enter the hash to search: ",
    "saliendo": "Exiting...",
    "opcion_invalida": "Invalid option.",
})

traducciones["es"].update({
    "longitud": "Longitud: ",
    "error_entrada": "Error de entrada.",
    "caracteres": "Caracteres:",
    "minusculas": "Minusculas",
    "mayusculas": "Mayusculas",
    "numeros": "Numeros",
    "combinado": "Combinado",
    "tipo": "Tipo: ",
    "algoritmos_soportados": "\n[INFO] Algoritmos soportados:\n",
    "presiona_enter": "Presiona Enter para volver al menu...",
})

traducciones["en"].update({
    "longitud": "Length: ",
    "error_entrada": "Input error.",
    "caracteres": "Characters:",
    "minusculas": "Lowercase",
    "mayusculas": "Uppercase",
    "numeros": "Numbers",
    "combinado": "Combined",
    "tipo": "Type: ",
    "algoritmos_soportados": "\n[INFO] Supported algorithms:\n",
    "presiona_enter": "Press Enter to return to the menu...",
})

traducciones["es"].update({
    "configuraciones_adicionales": "\n[INFO] Configuraciones adicionales para el ataque:\n",
    "usar_reglas": "¿Deseas usar un archivo de reglas? (s/n): ",
    "activar_notificaciones": "¿Deseas activar notificaciones por Discord? (s/n): ",
    "notificaciones_activadas": "[INFO] Notificaciones de Discord configuradas.",
    "notificaciones_desactivadas": "[INFO] Notificaciones de Discord desactivadas.",
})

traducciones["en"].update({
    "configuraciones_adicionales": "\n[INFO] Additional configurations for the attack:\n",
    "usar_reglas": "Do you want to use a rules file? (y/n): ",
    "activar_notificaciones": "Do you want to enable Discord notifications? (y/n): ",
    "notificaciones_activadas": "[INFO] Discord notifications configured.",
    "notificaciones_desactivadas": "[INFO] Discord notifications disabled.",
})

if __name__ == "__main__":
    try:
        validar_dependencias()
        configuracion["ruta_hashcat"] = buscar_hashcat()
        while True:
            menu()
    except Exception as e:
        print(Colores.rojo + f"[!] Error inesperado al iniciar el programa: {e}" + Colores.reset)
        logging.error(f"Error inesperado al iniciar el programa: {e}", exc_info=True)
        sys.exit(1)
