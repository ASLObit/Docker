import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PLACA = os.getenv("PLACA", "LKQ163")
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

def check_simit(placa):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")

    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get("https://www.simit.org.co/")

    try:
        print("Esperando el elemento con ID 'placa'...")
        wait = WebDriverWait(driver, 30) # Aumentar el tiempo de espera a 30 segundos
        element = wait.until(EC.presence_of_element_located((By.ID, "placa")))
        element.send_keys(placa)
        
        print("Esperando el botón de búsqueda...")
        button = wait.until(EC.element_to_be_clickable((By.ID, "buscar")))
        button.click()
        
    except Exception as e:
        print(f"Error esperando o encontrando el elemento: {e}")
        driver.quit()
        return "ERROR_EN_SCRAPING"

    time.sleep(10)

    result = "NO TIENE COMPARENDOS"
    if "comparendo" in driver.page_source.lower():
        result = "TIENE COMPARENDOS"

    driver.quit()
    return result

def send_to_homeassistant(message):
    print("Intentando enviar notificación a Home Assistant...")
    if HA_URL and HA_TOKEN:
        url = f"{HA_URL}/api/services/persistent_notification/create"
        headers = {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}
        payload = {"title": "Reporte SIMIT", "message": message}
        # Agregar `verify=False` para ignorar la verificación SSL
        requests.post(url, headers=headers, json=payload, verify=False)
        print("Notificación enviada.")
    else:
        print("HA_URL o HA_TOKEN no están configurados. No se enviará notificación.")

def job():
    print(f"Ejecutando tarea a las {time.strftime('%H:%M:%S')}")
    status = check_simit(PLACA)
    send_to_homeassistant(f"Placa {PLACA}: {status}")

if __name__ == "__main__":
    job() # Se ejecuta de inmediato para pruebas