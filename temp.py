from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import keyboard
import time

# Configura el servicio de ChromeDriver
chrome_driver_path = "chromedriver.exe"  # Reemplaza con tu ruta
chrome_service = ChromeService(chrome_driver_path)
chrome_service.start()

# Configura las opciones del navegador
options = webdriver.ChromeOptions()
# Configura opciones adicionales si es necesario
# Deshabilita las notificaciones
options.add_argument("--disable-notifications")

# Inicializa el WebDriver utilizando el servicio y las opciones
browser = webdriver.Chrome(service=chrome_service, options=options)

# Abre la página web
browser.get('https://www.google.com/')

for i in range(0, 300):
    try:
        # Espera a que el elemento del QR esté presente
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#APjFqb')))
        # Hacer click en el botón de nuevo mensaje
        browser.find_element(By.CSS_SELECTOR, '#APjFqb').click()

        # Agregar número de teléfono
        browser.find_element(By.CSS_SELECTOR, '#APjFqb').send_keys("Hola")

        # Enviar mensaje con Enter
        browser.find_element(By.CSS_SELECTOR, '#APjFqb').send_keys(Keys.ENTER)

        # Espera un momento para que el mensaje se envíe
        time.sleep(2)

        # Simula la combinación de teclas Alt + Flecha Izquierda
        keyboard.press('alt')
        keyboard.press_and_release('left')
        keyboard.release('alt')
        
    except StaleElementReferenceException as e:
        print("Error: Elemento de página obsoleto. ", str(e))
    except ElementClickInterceptedException as e:
        print("Error: Intercepción de clic en el elemento. ", str(e))
    except Exception as e:
        print("Ocurrió un error inesperado: ", str(e))

    finally:
        time.sleep(30)
        # Cierra el navegador y detiene el servicio
        browser.quit()
        chrome_service.stop()
