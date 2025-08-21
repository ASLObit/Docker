# Usa una imagen que ya tiene Python y Selenium preinstalados
FROM seleniarm/python-selenium

# Configura el directorio de trabajo
WORKDIR /app

# Copia e instala las dependencias de Python
COPY app/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY app/ .

CMD ["python3", "simit_checker.py"]