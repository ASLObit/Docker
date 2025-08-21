FROM selenium/standalone-chrome:latest

USER root

# Instalar Python y pip
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de dependencias
COPY app/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Cambiar al usuario seluser para mejorar la seguridad
USER seluser

# Definir el punto de entrada que ejecuta el script directamente
ENTRYPOINT ["python3", "/app/simit_checker.py"]