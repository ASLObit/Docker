# Usa una imagen base oficial de Python, versión 3.9, en su variante slim para optimizar el tamaño.
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor a /app.
# Todos los comandos subsecuentes se ejecutarán desde esta ubicación.
WORKDIR /app

# Copia solo el archivo de requisitos.
# Esto optimiza el cache de Docker. Si el archivo de dependencias no cambia,
# la siguiente capa de instalación no tendrá que ser reconstruida.
COPY requirements.txt .

# Instala las dependencias del script.
# La única dependencia necesaria para la solución propuesta es `requests`.
RUN pip install -r requirements.txt

# Copia el script de la aplicación.
# Esta capa es la que cambia con mayor frecuencia, por lo que se ubica al final.
COPY simit_checker.py .

# Define el comando que se ejecutará cuando el contenedor se inicie.
# CMD es ideal para un script que debe ser ejecutado con argumentos.
CMD ["python3", "simit_checker.py"]