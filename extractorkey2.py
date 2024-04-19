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
archivo = "checarlola2.txt"

# Verificar si el archivo existe
try:
    with open(archivo, "r") as file:
        urls = file.read().splitlines()
except FileNotFoundError:
    print(f"El archivo {archivo} no existe.")
    exit(1)

# Lista para almacenar los resultados de patrones
resultados = []

# Diccionario de patrones a buscar
patrones_busqueda = {
    "Extracted-token": r"(?i)(([a-z0-9]+)[-|_])?(key|password|passwd|pass|pwd|private|credential|auth|cred|creds|secret|access|token|secretaccesskey)([-|_][a-z]+)?(\\s)*(:|=)+",
    "Conexion_aks": r"DefaultEndpointsProtocol=https;AccountName=[^;]+;AccountKey=[^;]+;EndpointSuffix=core\.windows\.net",
    "Token_JWT": r"eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*",
    "Google-api-key": r"(?i)AIza[0-9A-Za-z\-_]{35}",
    "Authorization-Basic": r"(?i)(Authorization:\sbasic\s+[a-z0-9=:_\-+/]{5,100})",
    "Authorization-Bearer": r"(?i)(Authorization:\sbearer\s+[a-z0-9=:_\-\.+/]{5,100})",
    # Agrega más patrones según sea necesario
}

# Función para procesar una URL y buscar patrones
def procesar_url(url):
    print(f"{Fore.GREEN}{Style.BRIGHT}[✓] Procesando URL: {Style.RESET_ALL}{url}")
    try:
        response = requests.get(url, timeout=7)
        response.raise_for_status()
        contenido = response.text
        patrones_encontrados = {}
        for nombre, patron in patrones_busqueda.items():
            coincidencias = re.findall(patron, contenido)
            if coincidencias:
                patrones_encontrados[nombre] = coincidencias
        if patrones_encontrados:
            resultados.append((url, patrones_encontrados))
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}{Style.BRIGHT}[x] Error al procesar URL: {Style.RESET_ALL}{url}")

# Usar ThreadPoolExecutor para procesar las URL concurrentemente
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {executor.submit(procesar_url, url): url for url in urls}

    for future in concurrent.futures.as_completed(futures):
        future.result()

# Banner FIN PROCESO
    print(f"{Fore.CYAN}{Style.BRIGHT}================= PATRONES BUSCADOS ================={Style.RESET_ALL}")

# Imprimir los valores buscados
for clave, valor in patrones_busqueda.items():
    print(f"{Fore.GREEN}{Style.BRIGHT}[☀] {clave} : {valor}{Style.RESET_ALL}")

# Imprimir margen
print(f"{Fore.CYAN}{Style.BRIGHT}================= RESULTADO DE LAS BUSQUEDAS ================={Style.RESET_ALL}")

# Imprimir resultados al final
for url, patrones_encontrados in resultados:
    print(f"{Fore.YELLOW}{Style.BRIGHT}[♥] Patrones encontrados en la URL {url}:{Style.RESET_ALL}")
    for nombre, coincidencias in patrones_encontrados.items():
        print(f"{Fore.MAGENTA}{Style.BRIGHT}     {nombre}:{Style.RESET_ALL} {coincidencias}")
