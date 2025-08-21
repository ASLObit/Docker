FROM python:3.11-slim

# Instalar dependencias de Chrome y Selenium
RUN apt-get update && apt-get install -y \
    wget gnupg unzip cron \
    libnss3 libgconf-2-4 libxss1 libappindicator1 libindicator7 \
    fonts-liberation libatk-bridge2.0-0 libgtk-3-0 xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Descargar e instalar Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# Instalar Chromedriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1) && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0.5359.71/chromedriver_linux64.zip" || true && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ || true && \
    rm /tmp/chromedriver.zip

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
