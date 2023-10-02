import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
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

try:
    # Inicializa el WebDriver utilizando el servicio y las opciones
    browser = webdriver.Chrome(service=chrome_service, options=options)

    # Abre la página web
    browser.get('https://messages.google.com/web/conversations')

    # Espera a que el elemento del QR esté presente
    qr_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'mw-qr-code img')))

    # Espera a que la imagen del QR cargue
    WebDriverWait(browser, 10).until(lambda driver: qr_element.get_attribute("complete"))

    # Espera a que cambie el src del elemento del QR (indicando que se escaneó)
    WebDriverWait(browser, 60).until(EC.staleness_of(qr_element))

    # Agrega tu lógica aquí para lo que quieras hacer después de escanear el QR
    # Por ejemplo, puedes imprimir un mensaje indicando que el QR se ha escaneado
    print("El QR se ha escaneado.")

    # Espera a que aparezca el botón
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-main-nav > div > mw-fab-link > a'))).click()

    # Buscar el elemento de nuevo mensaje
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-main-nav > div > mw-fab-link > a > span.mdc-button__label')))

    # hacer click en el boton de nuevo mensaje
    browser.find_element(By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-main-nav > div > mw-fab-link > a > span.mdc-button__label').click()

    # hacer click en la entrada de nuevo mensaje
    browser.find_element(By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-new-conversation-container > mw-new-conversation-sub-header > div > div.input-container > mw-contact-chips-input > div > div > input').click()

    # agregar numero de telefono
    browser.find_element(By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-new-conversation-container > mw-new-conversation-sub-header > div > div.input-container > mw-contact-chips-input > div > div > input').send_keys("3174466434")

    # seleccionar el numero ingresado
    browser.find_element(By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-new-conversation-container > div > mw-contact-selector-button > button').click()
    
    # Espera a que la casilla de texto esté presente y sea visible
    texto_area = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'mws-autosize-textarea textarea')))

    # Escribir mensaje 
    browser.find_element(By.CSS_SELECTOR, 'mws-autosize-textarea textarea').send_keys("Mensaje Bonito")

    # Enviar mensaje con Enter
    browser.find_element(By.CSS_SELECTOR, 'mws-autosize-textarea textarea').send_keys(Keys.ENTER)

    # Pega el texto en el campo de entrada usando la combinación de teclas "Control + V"
    ActionChains(browser).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    
    # Enviar imagen con Enter
    browser.find_element(By.CSS_SELECTOR, 'mws-autosize-textarea textarea').send_keys(Keys.ENTER)
    
    """
    # Esperar a que aparezca la ventana de explorador de archivos
    ventana_explorador_archivos = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'selector_de_la_ventana_explorador_archivos')))

    # Pegar la ruta de la imagen en el campo de explorador de archivos
    ruta_de_la_imagen = 'ruta_de_la_imagen'  # Reemplaza con la ruta real de tu imagen
    ventana_explorador_archivos.send_keys(ruta_de_la_imagen)

    # Presionar Enter para cargar la imagen
    ventana_explorador_archivos.send_keys(Keys.ENTER)

    # Hacer clic en el botón de enviar mensaje
    browser.find_element(By.CSS_SELECTOR, 'selector_del_boton_enviar_mensaje').click()
    # hacer click en el boton de nuevo mensaje
    browser.find_element(By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-main-nav > div > mw-fab-link > a').click()
    """
    time.sleep(6)
        
except StaleElementReferenceException as e:
    print("Error: Elemento de página obsoleto. ", str(e))
except ElementClickInterceptedException as e:
    print("Error: Intercepción de clic en el elemento. ", str(e))
except Exception as e:
    print("Ocurrió un error inesperado: ", str(e))


finally:
    # Cierra el navegador y detiene el servicio
    browser.quit()
    chrome_service.stop()