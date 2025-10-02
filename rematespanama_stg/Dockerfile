# rematespanamastg_stg/Dockerfile
FROM odoo:18.0

USER root
# Copiamos configuración y addons desde el repo al contenedor
COPY rematespanamastg-config/odoo.conf /etc/odoo/odoo.conf
COPY rematespanamastg-addons/ /mnt/extra-addons/

# Ajusta permisos para el usuario odoo (UID=101 en la imagen oficial)
RUN chown -R odoo:odoo /etc/odoo /mnt/extra-addons \
    && chmod -R a+rX /mnt/extra-addons

# (Opcional) instala dependencias Python si tuvieras requirements.txt
# RUN pip3 install --no-cache-dir -r /mnt/extra-addons/requirements.txt || true

USER odoo
