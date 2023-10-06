from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.keys import Keys
while True:
    chrome_driver_path = "chromedriver.exe"  # Reemplaza con tu ruta
    chrome_service = ChromeService(chrome_driver_path)

    chrome_service.start()
    rutaCarpeta = r"C:\Users\ASUS\Desktop\MGS_Selenium\Chrome_05-10-2023_15-15-49"

    # Configura las opciones del navegador
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument('user-data-dir='+rutaCarpeta)

    # Inicializa el WebDriver utilizando el servicio y las opciones
    browser = webdriver.Chrome(service=chrome_service, options=options)

    # Abre la página web
    browser.get('https://messages.google.com/web/conversations')
    time.sleep(5)
    cont=0
     # agregar numero de telefono
    browser.find_element(By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-new-conversation-container > mw-new-conversation-sub-header > div > div.input-container > mw-contact-chips-input > div > div > input').send_keys("3174466432")

    # seleccionar el numero ingresado
    browser.find_element(By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-new-conversation-container > div > mw-contact-selector-button > button').click()

    MensajeMasivo="hola\newf"
    for i in range(1, 300):
        
        cont+=1
        try:
            
            
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
            print("Se ha eliminado chat"+str(cont))
        except:
            pass
        
    
