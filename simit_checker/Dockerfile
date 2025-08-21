FROM python:3.11-slim

# Asegurar que el sistema tenga acceso a internet y repositorios
RUN apt-get update -y && apt-get install -y curl && \
    curl -s https://deb.debian.org/debian/ || { echo "No hay conexión a internet"; exit 1; }

# Instalar dependencias de Chrome y Selenium
RUN apt-get update && apt-get install -y \
    wget gnupg unzip cron \
    libnss3 libgconf-2-4 libxss1 libappindicator1 libindicator7 \
    fonts-liberation libatk-bridge2.0-0 libgtk-3-0 xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Descargar e instalar Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# Instalar Chromedriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1) && \
    wget -q "https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0.5359.71/chromedriver_linux64.zip" -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

WORKDIR /app

# Dependencias Python
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar app
COPY app/ .

# Copiar cronjob
COPY app/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
