#!/bin/bash

# Crear cronjob para correr cada día a las 9 AM
echo "0 9 * * * root python /app/simit_checker.py >> /var/log/cron.log 2>&1" > /etc/cron.d/simit-cron

chmod 0644 /etc/cron.d/simit-cron
crontab /etc/cron.d/simit-cron

# Iniciar cron y quedarse corriendo
cron -f
