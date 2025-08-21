FROM python:3.12-slim

WORKDIR /app

# Copia e instala las dependencias desde la carpeta app
COPY app/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "simit_checker.py"]