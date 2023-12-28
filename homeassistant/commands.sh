#!/bin/sh

# Instalar curl y gdrive si no están instalados
if ! command -v curl &> /dev/null; then
    echo "curl no está instalado. Instalando..."
    apk --no-cache add curl
fi

if ! command -v gdrive &> /dev/null; then
    echo "gdrive no está instalado. Instalando..."
    curl -o /usr/local/bin/gdrive https://github.com/prasmussen/gdrive/releases/download/2.1.0/gdrive-linux-amd64
    chmod +x /usr/local/bin/gdrive
fi

# Descargar el archivo utilizando curl
curl -o /config/commands.sh https://raw.githubusercontent.com/ASLObit/Docker/main/homeassistant/commands.sh

# Subir el archivo a Google Drive
gdrive upload /config/backups/$(date +\%Y\%m\%d_\%H\%M\%S).tar --parent 1D0RP0i2ZWOc30jKMooqtgg9N2UdEIuR_
