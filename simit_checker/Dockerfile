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
COPY app/entrypoint.sh /entrypoint.sh
COPY app/simit_checker.py .
RUN chmod +x /entrypoint.sh

# Cambiar al usuario selenium
USER seluser

ENTRYPOINT ["/entrypoint.sh"]
