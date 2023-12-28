#!/bin/sh

Creación del backup
docker exec -it hassio_homeassistant hassio backup

Copia del backup a la carpeta de descargas
docker cp hassio_homeassistant:/config/backups/$(date +\%Y\%m\%d_\%H\%M\%S).tar /downloads
# Subida del backup a Google Drive
docker exec -it hassio_gdrive gdrive upload /downloads/$(date +%Y%m%d_%H%M%S).tar --parent 1D0RP0i2ZWOc30jKMooqtgg9N2UdEiU
