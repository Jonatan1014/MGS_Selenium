from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import openpyxl
import time
MensajeMasivo = "hola"

libro = openpyxl.load_workbook(r"C:\Users\farud\OneDrive\Escritorio\MGS_Selenium\400.xlsx")
hoja = libro["Hoja1"]
# Configura el servicio de ChromeDriver
chrome_driver_path = "chromedriver.exe"  # Reemplaza con tu ruta
chrome_service = ChromeService(chrome_driver_path)
chrome_service.start()

# Configura las opciones del navegador
options = webdriver.ChromeOptions()
# Configura opciones adicionales si es necesario
# Deshabilita las notificaciones
options.add_argument("--disable-notifications")
options.add_argument("--remote-debugging-port=9222")
options.add_argument(r'user-data-dir=C:\Users\farud\OneDrive\Escritorio\MGS_Selenium\Google Chrome')

# Inicializa el WebDriver utilizando el servicio y las opciones
browser = webdriver.Chrome(service=chrome_service, options=options)

# Abre la página web
# Abre la página web
browser.get('https://messages.google.com/web/conversations/new')
# Espera hasta que el elemento "loader" no sea visible
WebDriverWait(browser, 20).until(EC.invisibility_of_element_located((By.ID, 'loader')))

WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-new-conversation-container > mw-new-conversation-sub-header > div > div.input-container > mw-contact-chips-input > div > div > input'))).click()

cont = 0
for fila in hoja.iter_rows(min_row=1, values_only=True):  
    Celular = " - ".join(map(str, fila))
    


    try:
        
        # agregar numero de telefono
        campo_entrada = browser.find_element(By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-new-conversation-container > mw-new-conversation-sub-header > div > div.input-container > mw-contact-chips-input > div > div > input').send_keys(Celular)
        
            
        # seleccionar el numero ingresado
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-new-conversation-container > div > mw-contact-selector-button > button'))).click()
   
        # Espera hasta que el botón sea clickeable
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-e2e-next-button]'))).click()
        # Espera a que la casilla de texto esté presente y sea visible
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'mws-autosize-textarea textarea')))

        # Dividir el mensaje en párrafos
        parrafos = MensajeMasivo.split('\n')

        # Escribir cada párrafo en el área de texto
        for i, parrafo in enumerate(parrafos):
            # Escribir el párrafo actual
            browser.find_element(By.CSS_SELECTOR, 'mws-autosize-textarea textarea').send_keys(parrafo)

            # Si no es el último párrafo, enviar con "Shift + Enter" para empezar uno nuevo
            if i < len(parrafos) - 1:
                ActionChains(browser).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()

        # Enviar el último párrafo
        browser.find_element(By.CSS_SELECTOR, 'mws-autosize-textarea textarea').send_keys(Keys.ENTER)

        
        cont=cont+1
        print(cont)
        
        
                
    except StaleElementReferenceException as e:
        print("Error: Elemento de página obsoleto. ", str(e))
    except ElementClickInterceptedException as e:
        print("Error: Intercepción de clic en el elemento. ", str(e))
    except Exception as e:
        print("Ocurrió un error inesperado: ", str(e))
        


print("Mensaje Grupos Enviado")
time.sleep(3)
# Cierra el navegador y detiene el servicio
browser.quit()
chrome_service.stop()
print("Envio completado")
libro.close()
