import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

PLACA = os.getenv("PLACA", "LKQ163")
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

def check_simit(placa):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")

    # Conectarse al servidor de Selenium en el contenedor
    driver = RemoteWebDriver(
        command_executor='http://localhost:4444/wd/hub',
        options=options
    )
    driver.get("https://www.simit.org.co/")

    # Usar esperas explícitas para una ejecución más robusta
    try:
        wait = WebDriverWait(driver, 20)  # Espera hasta 20 segundos
        element = wait.until(EC.presence_of_element_located((By.ID, "placa")))
        element.send_keys(placa)
        
        button = wait.until(EC.element_to_be_clickable((By.ID, "buscar")))
        button.click()
        
    except Exception as e:
        print(f"Error esperando o encontrando el elemento: {e}")
        driver.quit()
        return "ERROR_EN_SCRAPING"

    # Esperar a que la página cargue los resultados
    time.sleep(10)

    # Verificar si aparece el texto de comparendos
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

if __name__ == "__main__":
    job() # Se ejecuta de inmediato para pruebas