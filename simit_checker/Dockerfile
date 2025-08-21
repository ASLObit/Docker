FROM python:3.12-slim

WORKDIR /app

# Copiar dependencias Python
COPY app/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY app/ .

CMD ["python3", "simit_checker.py"]