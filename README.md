# Recovery-File-macOS

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![macOS](https://img.shields.io/badge/macOS-Compatible-brightgreen)

## Descripción del Proyecto

**Recovery-File-macOS** es un script avanzado de Python diseñado para realizar una búsqueda profunda en los sectores del disco duro de macOS y recuperar archivos eliminados con extensión `.mp4`. Utiliza herramientas de análisis forense como `sleuthkit` para garantizar una recuperación efectiva y precisa de los archivos.

## Características

- **Búsqueda Profunda**: Realiza una búsqueda exhaustiva en los sectores del disco duro para encontrar archivos `.mp4` eliminados.
- **Recuperación Eficiente**: Recupera archivos eliminados y los guarda en una ubicación especificada por el usuario.
- **Interfaz de Usuario Intuitiva**: Utiliza la biblioteca `rich` para proporcionar una interfaz de usuario amigable y visualmente atractiva.
- **Registro de Actividades**: Registra todas las actividades y errores en un archivo de log para facilitar la depuración.

## Requisitos

- macOS
- Python 3.8 o superior
- `sleuthkit`
- `rich`

## Instalación

1. **Clonar el Repositorio**:

   ```sh
    git clone https://github.com/CodeGeekR/Recovery-File-macOS
    cd Recovery-File-macOS

   ```

2. **Instalar Dependencias**:
   ```sh
    pip install rich
    brew install sleuthkit
   ```

## Uso

1. **Ejecutar el Script**:

   ```sh
    python recovery.py
   ```

2. **Siga las instrucciones en pantalla para recuperar archivos eliminados**.

## Contribución

Las contribuciones son bienvenidas. Siéntete libre de abrir un problema o enviar una solicitud de extracción.

## Licencia

Distribuido bajo la licencia MIT. Consulte `LICENSE` para obtener más información.

## Contacto

Autor - [samuraidev](https://www.samuraidev.engineer)
