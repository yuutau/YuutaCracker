
import os
import subprocess
import sys
import time
import json
import logging
import requests
import shutil
from shutil import which
from datetime import datetime
import signal
import ctypes
import hashlib

# ct ppl on top
# dependencias papu

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("[INFO] Instalando dependencia 'deep-translator'...")
    os.system(f"{sys.executable} -m pip install deep-translator")
    from deep_translator import GoogleTranslator

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


try:
    ascii_calavera_verde
except NameError:
    ascii_calavera_verde = """
  (CALAVERA ASCII)
"""

_cache_traducciones = {}

def traducir(texto, destino="es"):
    """
    Traduce texto a 'destino' usando deep_translator.GoogleTranslator si está disponible.
    Usa caché simple para evitar llamadas repetidas.
    Devuelve el texto original en caso de fallo o si GoogleTranslator no está disponible.
    """
    if texto is None:
        return ""
    destino = destino or "es"
    clave = f"{texto}|{destino}"
    if clave in _cache_traducciones:
        return _cache_traducciones[clave]
    if GoogleTranslator is None:
        return texto
    try:
        traducido = GoogleTranslator(source="auto", target=destino).translate(texto)
        _cache_traducciones[clave] = traducido
        return traducido
    except Exception as e:
        logging.warning(f"[WARN] No se pudo traducir \"{texto}\": {e}")
        return texto

def t(texto):
    """
    Wrapper simple para traducción dinámica.
    Solo traduce si configuracion['idioma'] != 'es' (evita llamadas innecesarias).
    Texto debe ser la frase legible en el idioma original (p. ej. español).
    """
    try:
        idioma = configuracion.get("idioma", "es")
    except Exception:
        idioma = "es"
    if idioma == "es":
        return texto
    return traducir(texto, destino=idioma)

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
LOGDIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOGDIR, exist_ok=True)
logfile = os.path.join(LOGDIR, f"cracking_{datetime.now().strftime('%Y%m%d')}.log")

logging.basicConfig(
    filename=logfile,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def log(msg, lvl="info"):
    if lvl == "info":
        logging.info(msg)
    elif lvl == "warning":
        logging.warning(msg)
    elif lvl == "error":
        logging.error(msg)
    try:
        print(msg)
    except Exception:
        pass

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
    "notificaciones_telegram": False,
    "telegram_token": "",
    "telegram_chatid": "",
})

# -----------------------------------------------------------------------------
# Algoritmos soportados
# -----------------------------------------------------------------------------
ALGORITMOS_HASH = {
    "0": "MD5",
    "100": "SHA1",
    "1400": "SHA256",
    "1700": "SHA512",
    "22000": "WPA/WPA2",
}

# -----------------------------------------------------------------------------
# Utilidades
# -----------------------------------------------------------------------------
def validar_entrada_hashcat():
    if not configuracion["ruta_hashcat"]:
        print(Colores.rojo + t("[!] Hashcat no está configurado correctamente.") + Colores.reset)
        return False
    return True

def enviar_notificacion_discord(mensaje):
    if not requests:
        return
    if configuracion.get("notificaciones_discord") and configuracion.get("webhook_discord"):
        try:
            data = {"content": mensaje}
            requests.post(configuracion["webhook_discord"], json=data, timeout=8)
            print(Colores.verde + t("[INFO] Notificación enviada a Discord.") + Colores.reset)
        except Exception as e:
            print(Colores.rojo + f"[!] Error al enviar notificación a Discord: {e}" + Colores.reset)
            logging.error(f"Error al enviar notificacion a Discord: {e}")

def cambiar_idioma():
    idioma = input("Idioma / Language (es/en): ").strip().lower()
    if idioma in ["es", "en"]:
        configuracion["idioma"] = idioma
        print(Colores.verde + t("[INFO] Idioma cambiado a ") + idioma + Colores.reset)
        # Opcional: limpiar cache en cambio de idioma
        _cache_traducciones.clear()
    else:
        print(Colores.rojo + "Idioma no válido. Selecciona 'es' o 'en'." + Colores.reset)

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def mostrar_banner():
    """
    Mantiene la animación EXACTA si las librerías están disponibles.
    Si no, imprime ascii simple.
    """
    try:
        if Anime and Center and Colors and Colorate:
            Anime.Fade(Center.Center(ascii_art), Colors.red_to_blue, Colorate.Vertical, interval=0.035, enter=True)
        else:
            print(ascii_art)
    except Exception:
        print(ascii_art)

def mostrar_calavera_verde():
    try:
        if Colorate and Center and Colors:
            print(Colorate.Vertical(Colors.purple_to_blue, Center.Center(ascii_calavera_verde)))
        else:
            print(ascii_calavera_verde)
    except Exception:
        print(ascii_calavera_verde)

def buscar_hashcat():
    hashcat_path = shutil.which("hashcat") or shutil.which("hashcat.exe")
    if hashcat_path and os.path.isfile(hashcat_path):
        return hashcat_path

    print(t("[INFO] Buscando hashcat.exe globalmente..."))

    rutas_comunes = [
        r"C:\Hashcat\hashcat.exe",
        r"C:\Program Files\hashcat\hashcat.exe",
        r"C:\Program Files (x86)\hashcat\hashcat.exe",
        os.path.join(os.getcwd(), "hashcat.exe"),
    ]
    for ruta in rutas_comunes:
        if os.path.isfile(ruta):
            print(f"[INFO] Encontrado: {ruta}")
            return ruta

    unidades = []
    try:
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(26):
            if bitmask & (1 << i):
                unidades.append(letras[i] + ":\\")
    except Exception:
        unidades = ["C:\\", "D:\\"]

    for unidad in unidades:
        try:
            for root, dirs, files in os.walk(unidad, topdown=True):
                dirs[:] = [d for d in dirs if d.lower() not in ["windows", "programdata", "appdata", "recycle.bin", "node_modules", "venv", ".git"]]
                if "hashcat.exe" in files:
                    ruta = os.path.join(root, "hashcat.exe")
                    print(f"[INFO] Encontrado: {ruta}")
                    return ruta
        except Exception:
            continue

    manual = input("Ruta de hashcat.exe (o Enter para omitir): ").strip().strip('"')
    if manual and os.path.isfile(manual):
        return manual

    print("[!] No se encontró hashcat.exe en todo el sistema.")
    return None

def asegurar_directorio_hashcat(path_hashcat):
    carpeta = os.path.dirname(path_hashcat) if path_hashcat else ""
    if carpeta:
        try:
            os.chdir(carpeta)
        except Exception:
            pass

def seleccionar_dispositivo(hashcat):
    try:
        print(Colores.cyan + "\nDispositivos disponibles:\n" + Colores.reset)
        resultado = subprocess.check_output([hashcat, "-I"], stderr=subprocess.STDOUT, text=True)
        print(resultado)
        dispositivo = input("ID de dispositivo a usar (ej. 1): ").strip()
        configuracion["dispositivo_preferido"] = dispositivo
    except subprocess.CalledProcessError as e:
        print(Colores.rojo + "[!] No se pudo detectar dispositivos:\n" + Colores.reset + str(e))

def generar_mascara_personalizada():
    try:
        longitud = input("Longitud (enter para cancelar): ").strip()
        if longitud == "":
            return None
        longitud = int(longitud)
    except ValueError:
        print(Colores.rojo + "Longitud inválida." + Colores.reset)
        return None

    print("Tipo de caracteres:")
    print("[1] Minúsculas")
    print("[2] Mayúsculas")
    print("[3] Números")
    print("[4] Alfanumérico (mix)")
    opcion = input("Selecciona tipo: ").strip()

    if opcion == "1":
        plantilla = "?l"
    elif opcion == "2":
        plantilla = "?u"
    elif opcion == "3":
        plantilla = "?d"
    elif opcion == "4":
        partes = ["?l", "?u", "?d"]
        mascara = "".join(partes[i % len(partes)] for i in range(longitud))
        print(Colores.verde + f"[INFO] Máscara generada: {mascara}" + Colores.reset)
        return mascara
    else:
        print(Colores.rojo + "Opción inválida." + Colores.reset)
        return None

    mascara = plantilla * longitud
    print(Colores.verde + f"[INFO] Máscara generada: {mascara}" + Colores.reset)
    return mascara

def guardar_clave_en_archivo(clave):
    try:
        ruta_archivo = os.path.join(BASE_DIR, "clave_encontrada.txt")
        with open(ruta_archivo, "a", encoding="utf-8") as file:
            file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {clave}\n")
        print(Colores.verde + f"\n[✓] Clave guardada en {ruta_archivo}" + Colores.reset)
        logging.info(f"Clave guardada: {clave}")
    except Exception as e:
        print(Colores.rojo + f"[!] Error al guardar la clave: {e}" + Colores.reset)
        logging.error(f"Error al guardar la clave: {e}")

def configurar_notificaciones_discord():
    if not requests:
        print(Colores.amarillo + "[WARN] requests no instalado, no se pueden configurar notificaciones de Discord." + Colores.reset)
        return
    respuesta = input(t("¿Activar notificaciones por Discord? (s/n): ")).strip().lower()
    configuracion["notificaciones_discord"] = respuesta == ("s" if configuracion["idioma"] == "es" else "y")
    if configuracion["notificaciones_discord"]:
        webhook = input(t("Introduce la URL del Webhook de Discord: ")).strip()
        configuracion["webhook_discord"] = webhook
        print(Colores.verde + t("[INFO] Notificaciones de Discord configuradas.") + Colores.reset)
    else:
        configuracion["webhook_discord"] = ""
        print(Colores.amarillo + t("[INFO] Notificaciones de Discord desactivadas.") + Colores.reset)

def generar_reporte_detallado(modo, archivo_hash, resultado, tiempo_inicio, tiempo_fin, archivo="reporte.txt"):
    try:
        if isinstance(tiempo_inicio, (int, float)):
            inicio = tiempo_inicio
        else:
            inicio = tiempo_inicio.timestamp()

        if isinstance(tiempo_fin, (int, float)):
            fin = tiempo_fin
        else:
            fin = tiempo_fin.timestamp()

        duracion = fin - inicio

        velocidad = "N/A"

        with open(archivo, "w", encoding="utf-8") as f:
            f.write("=========== REPORTE DE ATAQUE ===========\n")
            f.write(f"Modo: {modo}\n")
            f.write(f"Archivo Hash: {archivo_hash}\n")
            f.write(f"Resultado: {resultado}\n")
            f.write(f"Tiempo total: {duracion:.2f} segundos\n")
            f.write(f"Velocidad promedio: {velocidad}\n")
            f.write("-----------------------------------------\n")
            f.write("Generado por YuutaCracker\n")

        print(Colores.verde + "[OK] Reporte generado correctamente." + Colores.reset)

    except Exception as e:
        print(Colores.rojo + f"[!] Error al generar reporte: {e}" + Colores.reset)


def lanzar_hashcat(archivo, mascara, modo, diccionario=None, reglas=None, diccionarios=None, formato_hash="22000"):
    try:
        tiempo_inicio = datetime.now()
        hashcat = configuracion.get("ruta_hashcat")
        if not hashcat:
            print(Colores.rojo + t("[!] Ruta de Hashcat no definida. Asegúrate de que Hashcat esté instalado y configurado correctamente.") + Colores.reset)
            return
        if not validar_archivo(archivo):
            return
        if modo == "diccionario" and not diccionario:
            print(Colores.rojo + "[!] Diccionario no especificado para modo diccionario." + Colores.reset)
            return
        if modo == "diccionario" and not validar_archivo(diccionario):
            return

        args = [hashcat, "-m", formato_hash, "--optimized-kernel-enable", "--kernel-accel=64", "--kernel-loops=256", "--hwmon-temp-abort=90", "--force"]
        args += ["-a", "3" if modo == "bruteforce" else "0"]

        args.append(archivo)
        if modo == "bruteforce":
            args.append(mascara if mascara else "")
        else:
            args.append(diccionario if diccionario else "")

        if reglas:
            args += ["-r", reglas]
        if diccionarios:
            args += diccionarios

        if configuracion.get("dispositivo_preferido"):
            args += ["--backend-devices", configuracion["dispositivo_preferido"]]

        args += ["--status", "--status-json", "--session", "yuuta-session", "--logfile-disable", "--potfile-disable"]
        if configuracion.get("modo_sigiloso"):
            args.append("--quiet")

        print(Colores.cyan + t("[INFO] Hashcat iniciando...") + Colores.reset)
        logging.info("Hashcat iniciado con argumentos: " + " ".join(a for a in args if a))

        asegurar_directorio_hashcat(hashcat)
        proceso = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        start_time = time.time()
        fallo = False

        while True:
            if proceso.poll() is not None:
                break
            try:
                output = proceso.stdout.readline()
            except Exception:
                output = None

            if not output:
                time.sleep(0.02)
                continue

            output = output.strip()
            if not output:
                continue

            # Intentar parsear JSON
            parsed = None
            try:
                parsed = json.loads(output)
            except json.JSONDecodeError:
                if "error" in output.lower():
                    fallo = True
                    print(Colores.rojo + output + Colores.reset)
                else:
                    if not configuracion.get("modo_sigiloso", False):
                        print(output)
                continue
            except Exception as e:
                logging.error("Error parseando salida de hashcat: %s", e)
                continue

            try:
                mostrar_estado_hashcat(parsed, start_time)
                if 'password' in parsed:
                    clave = parsed['password']
                    log(Colores.verde + f"Clave encontrada: {clave}" + Colores.reset, "info")
                    guardar_clave_en_archivo(clave)
                    enviar_notificacion_discord(f"Clave encontrada: {clave}")
                    enviar_notificacion_telegram(f"Clave encontrada: {clave}")
                    generar_reporte_detallado(modo, archivo, clave, tiempo_inicio, datetime.now())
                    try:
                        proceso.terminate()
                    except Exception:
                        pass
                    break
            except Exception as e:
                logging.error("Error procesando JSON de hashcat: %s", e)

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
                enviar_notificacion_avanzada(f"Ataque terminado ({resultado}). Archivo: {archivo}")
        except Exception as e:
            logging.error("Error enviando notificación: %s", e)

        print(Colores.verde + "\n[✓] Ataque finalizado.\n" + Colores.reset)
        logging.info("Ataque finalizado.")
        enviar_notificacion_discord("Ataque finalizado.")
        enviar_notificacion_telegram("Ataque finalizado. Clave no encontrada.")
        # Generar reporte final sólo si no se generó uno con la clave (evitar duplicados)
        generar_reporte_detallado(modo, archivo, "No encontrada", tiempo_inicio, datetime.now())
        time.sleep(1)

    except Exception as e:
        print(Colores.rojo + f"[!] Error inesperado: {e}" + Colores.reset)
        logging.error(f"Error inesperado: {e}", exc_info=True)

def lanzar_hashcat_combinado(archivo, diccionario1, diccionario2, reglas=None, diccionarios=None, formato_hash="22000"):
    try:
        tiempo_inicio = datetime.now()
        hashcat = configuracion.get("ruta_hashcat")
        if not hashcat:
            print(Colores.rojo + t("[!] Ruta de Hashcat no definida.") + Colores.reset)
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

        if configuracion.get("dispositivo_preferido"):
            args += ["--backend-devices", configuracion["dispositivo_preferido"]]
        if configuracion.get("modo_sigiloso"):
            args.append("--quiet")

        asegurar_directorio_hashcat(hashcat)
        proceso = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

        print(Colores.cyan + t("[INFO] Hashcat iniciando en modo combinado...") + Colores.reset)
        logging.info("Hashcat iniciado en modo combinado con argumentos: " + " ".join(a for a in args if a))

        fallo = False

        while True:
            if proceso.poll() is not None:
                break
            try:
                output = proceso.stdout.readline()
            except Exception:
                output = None

            if not output:
                time.sleep(0.02)
                continue

            output = output.strip()
            if not output:
                continue

            try:
                data = json.loads(output)
            except json.JSONDecodeError:
                if "error" in output.lower():
                    fallo = True
                    print(Colores.rojo + output + Colores.reset)
                else:
                    if not configuracion.get("modo_sigiloso", False):
                        print(output)
                continue

            estado = mostrar_estado_hashcat(data)
            if estado == "error":
                fallo = True

            if 'password' in data:
                clave = data['password']
                log(Colores.verde + f"Clave encontrada: {clave}" + Colores.reset, "info")
                guardar_clave_en_archivo(clave)
                enviar_notificacion_discord(f"Clave encontrada: {clave}")
                enviar_notificacion_telegram(f"Clave encontrada: {clave}")
                generar_reporte_detallado("combinado", archivo, clave, tiempo_inicio, datetime.now())
                try:
                    proceso.terminate()
                except Exception:
                    pass
                break

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
                enviar_notificacion_avanzada(f"Ataque combinado terminado ({resultado}). Archivo: {archivo}")
        except Exception as e:
            logging.error("Error enviando notificación: %s", e)

        print(Colores.verde + "\n[✓] Ataque combinado finalizado.\n" + Colores.reset)
        logging.info("Ataque combinado finalizado.")
        enviar_notificacion_discord("Ataque combinado finalizado.")
        enviar_notificacion_telegram("Ataque combinado finalizado. Clave no encontrada.")
        generar_reporte_detallado("combinado", archivo, "No encontrada", tiempo_inicio, datetime.now())
        time.sleep(1)

    except Exception as e:
        print(Colores.rojo + f"[!] Error inesperado: {e}" + Colores.reset)
        logging.error(f"Error inesperado: {e}", exc_info=True)

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
                except Exception:
                    pass
            print(Colores.cyan + f"[INFO] Claves por segundo: {speed_total:,} H/s" + Colores.reset)

        if "progress" in data:
            prog = None
            total = None
            if isinstance(data["progress"], list) and len(data["progress"]) == 2:
                prog, total = data["progress"]
            elif isinstance(data["progress"], (int, float)):
                prog = data["progress"]
            if prog is not None and total:
                try:
                    pct = (prog / total) * 100 if total else 0
                    print(Colores.amarillo + f"[INFO] Progreso: {pct:.2f}% ({prog}/{total})" + Colores.reset)
                except Exception:
                    pass

        # Tiempo transcurrido
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
        with open(ruta_historial, "r", encoding="utf-8") as file:
            print(Colores.cyan + "\n[INFO] Historial de ataques:\n" + Colores.reset)
            print(file.read())
    except FileNotFoundError:
        print(Colores.amarillo + "[INFO] No hay historial disponible." + Colores.reset)

def seleccionar_diccionarios():
    diccionarios = []
    print(Colores.cyan + t("[INFO] Selecciona los diccionarios (escribe 'done' para terminar):") + Colores.reset)
    while True:
        diccionario = input("Diccionario: ").strip()
        if diccionario.lower() == "done":
            break
        if validar_archivo(diccionario):
            diccionarios.append(diccionario)
        else:
            print(Colores.rojo + "[!] Diccionario no válido." + Colores.reset)
    return diccionarios

def buscar_en_base_de_datos(hash_input, api_key_hashmob=None):
    try:
        posible = hash_input.strip()
        if len(posible) != 40 or not all(c in "0123456789abcdefABCDEF" for c in posible):
            sha1 = hashlib.sha1(posible.encode("utf-8")).hexdigest().upper()
        else:
            sha1 = posible.upper()

        prefix = sha1[:5]
        suffix = sha1[5:]

        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        resp = requests.get(url, timeout=10) if requests else None
        if not resp or resp.status_code != 200:
            print(Colores.amarillo + "[INFO] No se pudo consultar la base de datos HIBP." + Colores.reset)
        else:
            lines = resp.text.splitlines()
            for line in lines:
                parts = line.split(':')
                if len(parts) >= 2 and parts[0].strip().upper() == suffix:
                    count = parts[1].strip()
                    log(Colores.rojo + f"[!] Hash encontrado en HIBP (veces): {count}" + Colores.reset, "info")
                    return True

        print(Colores.verde + "[INFO] Hash no encontrado en HIBP u otras fuentes (básico)." + Colores.reset)
        return False
    except Exception as e:
        print(Colores.rojo + f"[!] Error al buscar en base de datos: {e}" + Colores.reset)
        return False

def seleccionar_reglas():
    reglas = input("Archivo de reglas (.rule): ").strip()
    if validar_archivo(reglas):
        return reglas
    else:
        print(Colores.rojo + "[!] Archivo de reglas no válido." + Colores.reset)
        return None

def enviar_notificacion_avanzada(mensaje):
    """
    Envía notificaciones por Telegram y/o Discord Webhook.
    Retorna True si al menos un método se envió correctamente.
    """
    exito = False

    try:
        token = configuracion.get("telegram_token")
        chat_id = configuracion.get("telegram_chatid")
        if token and chat_id and requests:
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
        if webhook and requests:
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

def enviar_notificacion_telegram(mensaje):
    if not requests:
        return
    if configuracion.get("notificaciones_telegram") and configuracion.get("telegram_token") and configuracion.get("telegram_chatid"):
        try:
            url = f"https://api.telegram.org/bot{configuracion['telegram_token']}/sendMessage"
            data = {"chat_id": configuracion['telegram_chatid'], "text": mensaje}
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print(Colores.verde + t("[INFO] Notificación enviada a Telegram.") + Colores.reset)
            else:
                print(Colores.rojo + t("[!] Error al enviar notificación a Telegram.") + Colores.reset)
        except Exception as e:
            print(Colores.rojo + f"[!] {t('[!] Error al enviar notificación a Telegram.')}: {e}" + Colores.reset)

def lanzar_ataque_hibrido(archivo, diccionario, mascara, reglas=None, diccionarios=None, formato_hash="22000"):
    try:
        tiempo_inicio = datetime.now()
        hashcat = configuracion.get("ruta_hashcat")
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

        if configuracion.get("dispositivo_preferido"):
            args += ["--backend-devices", configuracion["dispositivo_preferido"]]
        if configuracion.get("modo_sigiloso"):
            args.append("--quiet")

        print(Colores.cyan + t("[INFO] Hashcat iniciando en modo híbrido...") + Colores.reset)
        logging.info("Hashcat iniciado en modo híbrido con argumentos: " + " ".join(a for a in args if a))

        asegurar_directorio_hashcat(hashcat)
        proceso = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

        fallo = False

        while True:
            if proceso.poll() is not None:
                break
            try:
                output = proceso.stdout.readline()
            except Exception:
                output = None

            if not output:
                time.sleep(0.02)
                continue

            output = output.strip()
            if not output:
                continue

            try:
                data = json.loads(output)
            except json.JSONDecodeError:
                if "error" in output.lower() or "no such file" in output.lower():
                    fallo = True
                    print(Colores.rojo + output + Colores.reset)
                else:
                    if not configuracion.get("modo_sigiloso", False):
                        print(output)
                continue

            estado = mostrar_estado_hashcat(data)
            if estado == "error":
                fallo = True

            if 'password' in data:
                clave = data['password']
                log(Colores.verde + f"Clave encontrada: {clave}" + Colores.reset, "info")
                guardar_clave_en_archivo(clave)
                enviar_notificacion_discord(f"Clave encontrada: {clave}")
                enviar_notificacion_telegram(f"Clave encontrada: {clave}")
                generar_reporte_detallado("híbrido", archivo, clave, tiempo_inicio, datetime.now())
                try:
                    proceso.terminate()
                except Exception:
                    pass
                break

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
                enviar_notificacion_avanzada(f"Ataque híbrido terminado ({resultado}). Archivo: {archivo}")
        except Exception as e:
            logging.error("Error enviando notificación: %s", e)

        log(Colores.verde + "Ataque híbrido finalizado." + Colores.reset, "info")
        logging.info("Ataque híbrido finalizado.")
        enviar_notificacion_discord("Ataque híbrido finalizado.")
        enviar_notificacion_telegram("Ataque híbrido finalizado. Clave no encontrada.")
        generar_reporte_detallado("híbrido", archivo, "No encontrada", tiempo_inicio, datetime.now())
        time.sleep(1)

    except Exception as e:
        print(Colores.rojo + f"[!] Error al iniciar el ataque híbrido: {e}" + Colores.reset)
        logging.error(f"Error en ataque híbrido: {e}", exc_info=True)

# -----------------------------------------------------------------------------
# Validaciones y configuración de ataque
# -----------------------------------------------------------------------------
def validar_dependencias():
    if not requests:
        print(Colores.amarillo + "[WARN] 'requests' no está instalado. Algunas funciones (notificaciones, HIBP) estarán limitadas." + Colores.reset)
    else:
        print(Colores.verde + "[INFO] Dependencias esenciales disponibles." + Colores.reset)

def configurar_ataque(modo):
    print(Colores.cyan + t("\n[INFO] Configuraciones adicionales para el ataque:\n") + Colores.reset)
    usar_reglas = input(t("¿Deseas usar un archivo de reglas? (s/n): ")).strip().lower()
    reglas = seleccionar_reglas() if usar_reglas == ("s" if configuracion["idioma"] == "es" else "y") else None

    diccionarios = configurar_diccionarios_si_relevante(modo)

    usar_notificaciones_discord = input(t("¿Deseas activar notificaciones por Discord? (s/n): ")).strip().lower()
    if usar_notificaciones_discord == ("s" if configuracion["idioma"] == "es" else "y"):
        configurar_notificaciones_discord()

    usar_notificaciones_telegram = input(t("¿Activar notificaciones por Telegram? (s/n): ")).strip().lower()
    if usar_notificaciones_telegram == ("s" if configuracion["idioma"] == "es" else "y"):
        configurar_notificaciones_telegram()

    return reglas, diccionarios

def mostrar_algoritmos():
    print(Colores.cyan + t("\n[INFO] Algoritmos soportados:\n") + Colores.reset)
    for codigo, nombre in ALGORITMOS_HASH.items():
        print(f"{codigo}: {nombre}")
    print()
    input(Colores.amarillo + t("Presiona Enter para volver al menú...") + Colores.reset)

def seleccionar_archivo():
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
    except Exception:
        # Fallback: pedir ruta por consola
        ruta = input("Ruta del archivo (o Enter para cancelar): ").strip()
        if not ruta:
            return None
        return ruta.strip('"')

def validar_algoritmo_hash(hash_input):
    if hash_input not in ALGORITMOS_HASH:
        print(Colores.rojo + f"[!] Algoritmo de hash no soportado: {hash_input}" + Colores.reset)
        return False
    return True

def validar_archivo(ruta):
    if not ruta or not os.path.isfile(ruta):
        print(Colores.rojo + f"[!] Archivo no encontrado o inválido: {ruta}" + Colores.reset)
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
    if not requests:
        print(Colores.amarillo + "[WARN] requests no instalado, no se pueden configurar notificaciones de Telegram." + Colores.reset)
        return
    respuesta = input(t("¿Activar notificaciones por Telegram? (s/n): ")).strip().lower()
    configuracion["notificaciones_telegram"] = respuesta == ("s" if configuracion["idioma"] == "es" else "y")
    if configuracion["notificaciones_telegram"]:
        token = input(t("Introduce el token del bot de Telegram: ")).strip()
        chat_id = input(t("Introduce el ID del chat de Telegram: ")).strip()
        configuracion["telegram_token"] = token
        configuracion["telegram_chatid"] = chat_id
        print(Colores.verde + t("[INFO] Notificaciones de Telegram configuradas.") + Colores.reset)
    else:
        configuracion["telegram_token"] = ""
        configuracion["telegram_chatid"] = ""
        print(Colores.amarillo + t("[INFO] Notificaciones de Telegram desactivadas.") + Colores.reset)


def ejecutar_benchmark():
    try:
        hashcat = configuracion.get("ruta_hashcat")
        if not hashcat:
            print(Colores.rojo + t("[!] Ruta de Hashcat no definida.") + Colores.reset)
            return

        asegurar_directorio_hashcat(hashcat)

        print(Colores.verde + t("[INFO] Ejecutando benchmark de Hashcat...\n") + Colores.reset)

        proceso = subprocess.Popen(
            [hashcat, "-b"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        modo_actual = None
        speed_actual = None

        def imprimir_panel(modo, speed):
            print(Colores.azul + "╔══════════════════════════════════════════╗" + Colores.reset)
            print(Colores.azul + f"║  Hash-Mode: {modo:<30}║" + Colores.reset)
            print(Colores.azul + f"║  Speed:     {speed:<30}║" + Colores.reset)
            print(Colores.azul + "╚══════════════════════════════════════════╝\n" + Colores.reset)

        basura = [
            "You can use it",
            "Note:",
            "To disable",
            "Successfully initialized",
            "Failed to initialize",
            "Toolkit required",
            "Falling back",
            "timeout",
            "OpenCL API",
            "Benchmark relevant options",
            "optimized-kernel-enable",
        ]

        primera_linea = True

        for linea in proceso.stdout:
            linea = linea.strip()
            if not linea:
                continue

            if "hashcat (" in linea:
                if primera_linea:
                    print(Colores.verde + linea + Colores.reset)
                    primera_linea = False
                continue

            if any(x in linea for x in basura):
                continue

            if linea.startswith("----") or linea.startswith("===="):
                print(Colores.verde + linea + Colores.reset)
                continue

            if linea.startswith("* Hash-Mode"):
                modo_actual = linea.replace("* Hash-Mode", "").strip()
                continue

            if "Speed" in linea:
                speed_actual = linea.replace("Speed.#1.........:", "").strip()
                if modo_actual and speed_actual:
                    imprimir_panel(modo_actual, speed_actual)
                    modo_actual = None
                    speed_actual = None
                continue

            print(Colores.verde + linea + Colores.reset)

        proceso.wait()

        if proceso.returncode != 0:
            print(Colores.rojo + "[X] Benchmark falló o terminó con errores." + Colores.reset)
        else:
            print(Colores.verde + "[✓] Benchmark finalizado correctamente." + Colores.reset)

    except Exception as e:
        print(Colores.rojo + f"[!] Error en benchmark: {e}" + Colores.reset)

def _preload_menu_translations():
    keys = [
        "1) Mostrar algoritmos soportados",
        "2) Ataque Bruteforce (máscara)",
        "3) Ataque por Diccionario",
        "4) Ataque Combinado",
        "5) Ataque Híbrido",
        "6) Ver Historial",
        "7) Buscar hash en bases públicas",
        "8) Cambiar idioma",
        "9) Benchmark de Hashcat",
        "10) Salir",
        "Selecciona una opción: ",
        "Formato de hash (ej. 22000): ",
        "Introduce el hash a buscar: ",
        "Saliendo...",
        "Opción inválida."
    ]
    idioma = configuracion.get("idioma", "es")
    if idioma == "es" or GoogleTranslator is None:
        return
    for k in keys:
        try:
            _ = traducir(k, destino=idioma)
        except Exception:
            pass

def menu():
    limpiar_pantalla()
    mostrar_banner()
    mostrar_calavera_verde()

    opciones = [
        t("1) Mostrar algoritmos soportados"),
        t("2) Ataque Bruteforce (máscara)"),
        t("3) Ataque por Diccionario"),
        t("4) Ataque Combinado"),
        t("5) Ataque Híbrido"),
        t("6) Ver Historial"),
        t("7) Buscar hash en bases públicas"),
        t("8) Cambiar idioma"),
        t("9) Benchmark de Hashcat"),
        t("10) Salir"),
    ]
    for opcion in opciones:
        try:
            if Colorate and Colors:
                print(Colorate.Horizontal(Colors.red_to_yellow, opcion))
            else:
                print(opcion)
        except Exception:
            print(opcion)

    print()
    opcion = input(t("Selecciona una opción: ")).strip()

    if opcion == "1":
        mostrar_algoritmos()
    elif opcion == "2":
        formato_hash = input(t("Formato de hash (ej. 22000): ")).strip()
        if not validar_algoritmo_hash(formato_hash):
            return
        archivo = seleccionar_archivo()
        if not validar_archivo(archivo):
            return
        mascara = generar_mascara_personalizada()
        reglas, diccionarios = configurar_ataque(modo="bruteforce")
        lanzar_hashcat(archivo, mascara, "bruteforce", reglas=reglas, diccionarios=diccionarios, formato_hash=formato_hash)
    elif opcion == "3":
        formato_hash = input(t("Formato de hash (ej. 22000): ")).strip()
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
        formato_hash = input(t("Formato de hash (ej. 22000): ")).strip()
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
        formato_hash = input(t("Formato de hash (ej. 22000): ")).strip()
        if not validar_algoritmo_hash(formato_hash):
            return
        archivo = seleccionar_archivo()
        if not validar_archivo(archivo):
            return
        diccionario = seleccionar_archivo()
        if not validar_archivo(diccionario):
            return
        mascara = input("Máscara: ").strip()
        reglas, diccionarios = configurar_ataque(modo="hibrido")
        lanzar_ataque_hibrido(archivo, diccionario, mascara, reglas=reglas, diccionarios=diccionarios, formato_hash=formato_hash)
    elif opcion == "6":
        mostrar_historial()
    elif opcion == "7":
        hash_input = input(t("Introduce el hash a buscar: ")).strip()
        buscar_en_base_de_datos(hash_input)
    elif opcion == "8":
        cambiar_idioma()
    elif opcion == "9":
        ejecutar_benchmark()
    elif opcion == "10":
        print(t("Saliendo..."))
        logging.info("Programa finalizado por el usuario.")
        sys.exit(0)
    else:
        print(t("Opción inválida."))
    time.sleep(1)

if __name__ == "__main__":
    try:
        validar_dependencias()
        configuracion["ruta_hashcat"] = buscar_hashcat()

        _preload_menu_translations()

        while True:
            menu()

    except KeyboardInterrupt:
        print(Colores.rojo + "\n[!] Interrumpido por el usuario." + Colores.reset)
        sys.exit(0)
    except Exception as e:
        print(Colores.rojo + f"[!] Error inesperado al iniciar el programa: {e}" + Colores.reset)
        logging.error(f"Error inesperado al iniciar el programa: {e}", exc_info=True)
        sys.exit(1)
