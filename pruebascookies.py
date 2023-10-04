import pickle
import os.path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
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

# Verifica si existe información de sesión anterior
time.sleep(5)
if os.path.isfile('session_info.pkl'):
    with open('session_info.pkl', 'rb') as session_file:
        session_info = pickle.load(session_file)
        current_url = session_info.get('url', None)
        cookies = session_info.get('cookies', [])

    if current_url:
        browser.get(current_url)

    # Agrega las cookies almacenadas
    for cookie in cookies:
        browser.add_cookie(cookie)

# Si no hay información de sesión anterior, procede como antes
else:
    # Abre la página web
    browser.get('https://messages.google.com/web/conversations')

    # Espera a que el elemento del QR esté presente
    qr_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'mw-qr-code img')))

    # Espera a que la imagen del QR cargue
    WebDriverWait(browser, 10).until(lambda driver: qr_element.get_attribute("complete"))

    # Botón de recordar inicio de sesión
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mat-mdc-slide-toggle-1 > div'))).click()

    # Espera a que cambie el src del elemento del QR (indicando que se escaneó)
    WebDriverWait(browser, 60).until(EC.staleness_of(qr_element))

    # Agrega tu lógica aquí para lo que quieras hacer después de escanear el QR
    # Por ejemplo, puedes imprimir un mensaje indicando que el QR se ha escaneado
    print("El QR se ha escaneado.")

cont = 0 
for i in range(0, 11):
    try:
        # ... (código para enviar mensajes)
        
        # Espera a que aparezca el botón
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-main-nav > div > mw-fab-link > a'))).click()

        # Buscar el elemento de nuevo mensaje
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-main-nav > div > mw-fab-link > a > span.mdc-button__label')))

        # hacer click en el boton de nuevo mensaje
        browser.find_element(By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-main-nav > div > mw-fab-link > a > span.mdc-button__label').click()

        # agregar numero de telefono
        browser.find_element(By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-new-conversation-container > mw-new-conversation-sub-header > div > div.input-container > mw-contact-chips-input > div > div > input').send_keys("3174466432")

        # seleccionar el numero ingresado
        browser.find_element(By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-new-conversation-container > div > mw-contact-selector-button > button').click()
        
        # Espera a que la casilla de texto esté presente y sea visible
        texto_area = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'mws-autosize-textarea textarea')))
       
        # Escribir mensaje 
        browser.find_element(By.CSS_SELECTOR, 'mws-autosize-textarea textarea').send_keys("M")

        # Enviar mensaje con Enter
        browser.find_element(By.CSS_SELECTOR, 'mws-autosize-textarea textarea').send_keys(Keys.ENTER)
        
        cont+=1
        print(cont)
        

        # Guarda las cookies cada 10 mensajes
        if cont % 10 == 0:
            print("Guardando cookies...")
            cookies = browser.get_cookies()
            with open(f'cookies_{cont}.pkl', 'wb') as cookies_file:
                pickle.dump(cookies, cookies_file)

    except StaleElementReferenceException as e:
        print("Error: Elemento de página obsoleto. ", str(e))
    except ElementClickInterceptedException as e:
        print("Error: Intercepción de clic en el elemento. ", str(e))
    except Exception as e:
        print("Ocurrió un error inesperado: ", str(e))
    except:
        print("error")

# Antes de cerrar el navegador, guarda la URL actual y las cookies
current_url = browser.current_url
cookies = browser.get_cookies()

# Cierra el navegador y detiene el servicio
browser.quit()
chrome_service.stop()

# Guarda la URL y las cookies en un archivo
with open('session_info.pkl', 'wb') as session_file:
    pickle.dump({'url': current_url, 'cookies': cookies}, session_file)
