FROM selenium/standalone-chrome:latest

# Cambia al usuario root para poder instalar paquetes
USER root

# Instalar Python y pip
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de dependencias y ejecutar la instalación
COPY app/requirements.txt . [cite: 2]
RUN pip3 install --no-cache-dir -r requirements.txt [cite: 3, 5]

# Copiar el resto de la aplicación, incluyendo simit_checker.py y entrypoint.sh
COPY app/ . 

# Dar permisos de ejecución al entrypoint en su nueva ubicación (/app)
RUN chmod +x /app/entrypoint.sh

# Cambiar al usuario seluser para mejorar la seguridad
USER seluser

# Definir el punto de entrada del contenedor
ENTRYPOINT ["/app/entrypoint.sh"]