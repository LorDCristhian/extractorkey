import concurrent.futures
import requests
import re
from colorama import Fore, Style, init


# Banner
banner = """
  
 ██▀███  ▓█████ ▓█████▄ ▄▄▄█████▓▓█████ ▄▄▄       ███▄ ▄███▓
▓██ ▒ ██▒▓█   ▀ ▒██▀ ██▌▓  ██▒ ▓▒▓█   ▀▒████▄    ▓██▒▀█▀ ██▒
▓██ ░▄█ ▒▒███   ░██   █▌▒ ▓██░ ▒░▒███  ▒██  ▀█▄  ▓██    ▓██░
▒██▀▀█▄  ▒▓█  ▄ ░▓█▄   ▌░ ▓██▓ ░ ▒▓█  ▄░██▄▄▄▄██ ▒██    ▒██ 
░██▓ ▒██▒░▒████▒░▒████▓   ▒██▒ ░ ░▒████▒▓█   ▓██▒▒██▒   ░██▒
░ ▒▓ ░▒▓░░░ ▒░ ░ ▒▒▓  ▒   ▒ ░░   ░░ ▒░ ░▒▒   ▓▒█░░ ▒░   ░  ░
  ░▒ ░ ▒░ ░ ░  ░ ░ ▒  ▒     ░     ░ ░  ░ ▒   ▒▒ ░░  ░      ░
  ░░   ░    ░    ░ ░  ░   ░         ░    ░   ▒   ░      ░   
   ░        ░  ░   ░                ░  ░     ░  ░       ░    
"""

print(f"{Fore.RED}{Style.BRIGHT}{banner}{Style.RESET_ALL}")

# Banner INICIO PROCESO
print(f"{Fore.CYAN}{Style.BRIGHT}================= BUSQUEDAS DE COINCIDENCIAS ================={Style.RESET_ALL}")

# Nombre del archivo que contiene las líneas
archivo = "checar4.txt"

# Verificar si el archivo existe
try:
    with open(archivo, "r") as file:
        urls = file.read().splitlines()
except FileNotFoundError:
    print(f"El archivo {archivo} no existe.")
    exit(1)

# Lista para almacenar los resultados de patrones
resultados = []

# Función para procesar una URL y buscar patrones
def procesar_url(url):
    print(f"{Fore.GREEN}{Style.BRIGHT}[✓] Procesando URL: {Style.RESET_ALL}{url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        contenido = response.text
        patrones = re.findall(
            r"[A-Za-z0-9+/]{86}==|DefaultEndpointsProtocol=https;AccountName=[^;]+;AccountKey=[^;]+;EndpointSuffix=core\.windows\.net|eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*",
            contenido,
        )
        if patrones and any(len(p) > 0 for p in patrones):  # Verifica que haya patrones y que su longitud sea mayor a 0
            resultados.append((url, patrones))
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}{Style.BRIGHT}[x] Error al procesar URL: {Style.RESET_ALL}{url}")

# Usar ThreadPoolExecutor para procesar las URL concurrentemente
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {executor.submit(procesar_url, url): url for url in urls}

    for future in concurrent.futures.as_completed(futures):
        future.result()

# Banner FIN PROCESO
    #print(f"",end='\n')
    print(f"{Fore.CYAN}{Style.BRIGHT}================= RESULTADO DE LAS BUSQUEDAS ================={Style.RESET_ALL}")  
# Imprimir resultados al final
for url, patrones in resultados:  
    print(f"{Fore.YELLOW}{Style.BRIGHT}[♥] Patrones encontrados en la URL {url}:{Style.RESET_ALL} {patrones}")
