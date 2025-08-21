# Usa una imagen base con Python
FROM python:3.12-slim

# Instala las dependencias necesarias para Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    libnss3 \
    libx11-6 \
    libxrandr2 \
    libxext6 \
    libxcursor1 \
    libxfixes3 \
    libasound2 \
    libgbm1 \
    libpangocairo-1.0-0 \
    --no-install-recommends

# Instala Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Instala el Chromedriver compatible con el navegador
RUN LATEST_CHROMEDRIVER=$(wget -q -O - https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | grep -o '\"stable\":{\"version\":\"[0-9.]*\"' | cut -d ':' -f2 | tr -d '\"' | cut -d '.' -f1) \
    && CHROME_VERSION=$(google-chrome --version | cut -d ' ' -f3 | cut -d '.' -f1) \
    && DRIVER_VERSION=$(wget -q -O - https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | grep -o "\"version\": \"$CHROME_VERSION.*\"" | head -1 | cut -d':' -f2 | tr -d '\"' | cut -d',' -f1 | tr -d ' ' | tr -d '\n') \
    && wget -O chromedriver.zip $(wget -q -O - https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | grep -o "https://.*zip" | grep "chromedriver-linux64") \
    && unzip chromedriver.zip \
    && mv chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && rm chromedriver.zip \
    && rm -rf chromedriver-linux64

# Configura el directorio de trabajo
WORKDIR /app

# Copia e instala las dependencias de Python
COPY app/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY app/ .

CMD ["python3", "simit_checker.py"]