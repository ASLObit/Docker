FROM selenium/standalone-chrome:latest

USER root

# Instalar Python y pip
RUN apt-get update -y && apt-get install -y python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar dependencias Python
COPY app/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar toda la aplicación, incluyendo simit_checker.py
COPY app/ .

# Copiar y configurar entrypoint
RUN chmod +x /app/entrypoint.sh

# Cambiar al usuario selenium
USER seluser

# Corregir la ruta del punto de entrada
ENTRYPOINT ["/app/entrypoint.sh"]
