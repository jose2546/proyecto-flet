import time
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")

print("[TEST] Abriendo navegador...")
driver = webdriver.Chrome(options=options)

try:
    print("[TEST] Navegando a BetPlay...")
    driver.get("https://betplay.com.co")
    
    print("[TEST] Esperando 10 segundos para carga total...")
    time.sleep(10)
    
    # Capturamos todos los textos de la página para ver qué clases o nombres hay disponibles
    elementos = driver.find_elements(By.TAG_NAME, "div")
    textos = [el.text.strip() for el in elementos if el.text.strip()]
    
    print("\n--- TEXTOS DETECTADOS EN LA PÁGINA ---")
    # Imprime los primeros 15 textos encontrados para no saturar la consola
    for t in textos[:15]:
        print(f"- {t}")

except Exception as e:
    print(f"[ERROR] Ocurrió un fallo: {e}")
finally:
    driver.quit()
