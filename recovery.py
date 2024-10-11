import os
import shutil
from pathlib import Path
import logging
import subprocess
import unicodedata
import multiprocessing
import shlex
from rich import print as rprint
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

# Configuración de logging
logging.basicConfig(filename='recuperacion_archivos.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

console = Console()

def normalizar_ruta(ruta):
    """Normaliza una ruta para manejar caracteres especiales y espacios."""
    return Path(unicodedata.normalize('NFC', os.path.expanduser(ruta))).resolve()

def buscar_archivos_eliminados(carpeta, progress, task):
    """Realiza una búsqueda profunda en los sectores del disco duro para encontrar archivos eliminados con extensión .mp4."""
    archivos_encontrados = []
    carpeta_temp = Path("/tmp/recuperacion_archivos")

    if not carpeta_temp.exists():
        carpeta_temp.mkdir(parents=True, exist_ok=True)

    try:
        # Usar sleuthkit para buscar archivos .mp4 eliminados
        comando = f"sudo fls -r -d {shlex.quote(str(carpeta))} | grep -i '.mp4'"
        proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        for linea in proceso.stdout:
            if ".mp4" in linea.lower():
                archivo = linea.strip().split()[-1]
                if archivo not in archivos_encontrados:
                    archivos_encontrados.append(archivo)
                    progress.update(task, advance=1, description=f"Encontrados: {len(archivos_encontrados)}")

        proceso.wait()
        if proceso.returncode != 0:
            error = proceso.stderr.read()
            logging.error(f"Error en la búsqueda: {error}")
            console.print(f"[bold red]Error en la búsqueda: {error}[/bold red]")
    except Exception as e:
        logging.error(f"Error al buscar archivos: {str(e)}")
        console.print(f"[bold red]Error al buscar archivos: {str(e)}[/bold red]")

    return archivos_encontrados

def recuperar_archivo(archivo, destino):
    """Recupera un archivo y lo mueve al destino especificado."""
    try:
        nombre_archivo = Path(archivo).name
        ruta_destino = Path(destino) / nombre_archivo
        comando = f"sudo icat {shlex.quote(str(archivo))} > {shlex.quote(str(ruta_destino))}"
        subprocess.run(comando, shell=True, check=True)
        logging.info(f"Archivo recuperado: {archivo} -> {ruta_destino}")
        return True
    except Exception as e:
        logging.error(f"Error al recuperar el archivo {archivo}: {str(e)}")
        return False

def main():
    console.print("[bold green]Recuperación de Archivos Eliminados en macOS[/bold green]")

    carpeta_origen = Prompt.ask("Ingrese la ruta de la carpeta donde estaban los archivos")
    carpeta_origen = normalizar_ruta(shlex.split(carpeta_origen)[0])

    if not carpeta_origen.exists():
        console.print(f"[bold red]La carpeta especificada no existe: {carpeta_origen}[/bold red]")
        return

    with Progress(
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Buscando archivos eliminados...", total=None)
        archivos_encontrados = buscar_archivos_eliminados(carpeta_origen, progress, task)

    if not archivos_encontrados:
        console.print("[yellow]No se encontraron archivos para recuperar.[/yellow]")
        return

    console.print(f"[green]Se encontraron {len(archivos_encontrados)} archivos eliminados.[/green]")

    for i, archivo in enumerate(archivos_encontrados, 1):
        console.print(f"{i}. {archivo}")

    indices = Prompt.ask("Ingrese los números de los archivos que desea recuperar, separados por comas")
    indices = [int(i.strip()) - 1 for i in indices.split(",") if i.strip().isdigit()]

    archivos_seleccionados = [archivos_encontrados[i] for i in indices if i < len(archivos_encontrados)]

    carpeta_destino = Prompt.ask("Ingrese la ruta de la carpeta donde desea recuperar los archivos")
    carpeta_destino = normalizar_ruta(shlex.split(carpeta_destino)[0])

    if not carpeta_destino.exists():
        carpeta_destino.mkdir(parents=True, exist_ok=True)

    with console.status("Recuperando archivos..."):
        with multiprocessing.Pool() as pool:
            resultados = pool.starmap(recuperar_archivo, [(archivo, str(carpeta_destino)) for archivo in archivos_seleccionados])

    total_recuperados = sum(resultados)
    console.print(f"[green]Se han recuperado {total_recuperados} archivos en: {carpeta_destino}[/green]")

if __name__ == "__main__":
    main()