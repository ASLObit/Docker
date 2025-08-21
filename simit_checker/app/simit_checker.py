import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import schedule

PLACA = os.getenv("PLACA", "LKQ163")
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

def check_simit(placa):
    options = Options()
    
    # Conectarse al servidor de Selenium a través de la red de Docker
    driver = RemoteWebDriver(
        command_executor='http://selenium:4444/wd/hub',
        options=options
    )
    
    driver.get("https://www.simit.org.co/")

    try:
        wait = WebDriverWait(driver, 30)
        element = wait.until(EC.presence_of_element_located((By.ID, "placa")))
        element.send_keys(placa)
        
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
    if HA_URL and HA_TOKEN:
        url = f"{HA_URL}/api/services/persistent_notification/create"
        headers = {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}
        payload = {"title": "Reporte SIMIT", "message": message}
        requests.post(url, headers=headers, json=payload, verify=False)

def job():
    print(f"Ejecutando tarea a las {time.strftime('%H:%M:%S')}")
    status = check_simit(PLACA)
    send_to_homeassistant(f"Placa {PLACA}: {status}")

if __name__ == "__main__":
    job()