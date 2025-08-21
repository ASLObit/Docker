FROM python:3.12-slim

WORKDIR /app

# Copia e instala las dependencias
COPY app/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# El volumen se encarga de montar el resto de los archivos
CMD ["python3", "simit_checker.py"]