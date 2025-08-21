FROM python:3.11

# Verificar conexión a internet
RUN apt-get update -y && apt-get install -y curl && \
    curl -s https://deb.debian.org/debian/ || { echo "Error: No hay conexión a internet"; exit 1; }

# Instalar dependencias básicas y específicas
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    wget gnupg unzip \
    libnss3 libgtk-3-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Descargar e instalar una versión específica de Google Chrome
RUN wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.90-1_amd64.deb \
    && apt-get install -y --no-install-recommends ./google-chrome-stable_114.0.5735.90-1_amd64.deb \
    && rm google-chrome-stable_114.0.5735.90-1_amd64.deb

# Instalar Chromedriver compatible
RUN wget -q "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

WORKDIR /app

# Copiar dependencias Python
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY app/ .

# Copiar y configurar entrypoint
COPY app/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
