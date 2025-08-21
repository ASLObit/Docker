FROM selenium/standalone-chrome:latest

USER root

# Instalar Python, pip y cron
RUN apt-get update -y && apt-get install -y python3 python3-pip cron && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Crear directorio para tareas cron y asignar permisos
RUN mkdir -p /etc/cron.d && chmod 755 /etc/cron.d

WORKDIR /app

# Copiar dependencias Python
COPY app/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY app/ .

# Copiar y configurar entrypoint
COPY app/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copiar archivo de cron
COPY app/simit-cron /etc/cron.d/simit-cron
RUN chmod 644 /etc/cron.d/simit-cron

# Asegurar que los logs de cron sean accesibles
RUN touch /var/log/cron.log && chmod 644 /var/log/cron.log

# Cambiar al usuario selenium
USER seluser

ENTRYPOINT ["/entrypoint.sh"]
