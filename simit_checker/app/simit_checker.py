import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import schedule

PLACA = os.getenv("PLACA", "LKQ163")
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

def check_simit(placa):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.simit.org.co/")

    # Simular scraping (ajusta según el sitio real)
    time.sleep(5)
    driver.find_element(By.ID, "placa").send_keys(placa)
    driver.find_element(By.ID, "buscar").click()
    time.sleep(10)

    # Ejemplo: verificar si aparece texto de comparendos
    result = "NO TIENE COMPARENDOS"
    if "comparendo" in driver.page_source.lower():
        result = "TIENE COMPARENDOS"

    driver.quit()
    return result

def send_to_homeassistant(message):
    url = f"{HA_URL}/api/services/persistent_notification/create"
    headers = {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}
    payload = {"title": "Reporte SIMIT", "message": message}
    requests.post(url, headers=headers, json=payload)

def job():
    print(f"Ejecutando tarea a las {time.strftime('%H:%M:%S')}")
    status = check_simit(PLACA)
    send_to_homeassistant(f"Placa {PLACA}: {status}")

# Programar la tarea a las 9 AM (hora local, ajustada por TZ=America/Bogota)
schedule.every().day.at("09:00").do(job)

# Bucle principal
print("Iniciando scheduler. Esperando hasta las 9:00 AM...")
while True:
    schedule.run_pending()
    time.sleep(60)  # Revisar cada minuto
