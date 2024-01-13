import concurrent.futures
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def procesar_linea(linea):
    try:
        # Realizar solicitud HTTP a la URL y parsear el contenido
        url = linea.strip()
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Iterar sobre las etiquetas <script> y extraer rutas
        rutas = []
        for script_tag in soup.find_all('script', src=True):
            src = script_tag['src']
            ruta_absoluta = urljoin(url, src)
            rutas.append(ruta_absoluta)

        # Imprimir las rutas y almacenarlas en el archivo "checar.txt"
        with open("checar.txt", "a") as archivo_checar:
            for ruta in rutas:
                print(ruta)
                archivo_checar.write(f"{ruta}\n")

    except Exception:
        # Omitir cualquier error en la solicitud HTTP, el análisis HTML, o la escritura en el archivo
        pass

if __name__ == "__main__":
    # Leer el archivo de entrada
    with open("entrada4.txt", "r") as archivo:
        lineas = archivo.readlines()

    # Utilizar ThreadPoolExecutor para procesar líneas en paralelo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Mapear las líneas a las rutas usando hilos
        executor.map(procesar_linea, lineas)
