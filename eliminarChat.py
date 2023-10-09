from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
demora = 1
while True:
    
    
    
    chrome_driver_path = "chromedriver.exe"  # Reemplaza con tu ruta
    chrome_service = ChromeService(chrome_driver_path)

    chrome_service.start()
    rutaCarpeta = r"C:\Users\ASUS\Desktop\MGS_Selenium\Google 1"

    # Configura las opciones del navegador
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument('user-data-dir='+rutaCarpeta)

    # Inicializa el WebDriver utilizando el servicio y las opciones
    browser = webdriver.Chrome(service=chrome_service, options=options)

    # Abre la página web
    browser.get('https://messages.google.com/web/conversations')
    cont=0

    for i in range(1, 100):
        try:
            
            time.sleep(demora)
            WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-main-nav > mws-conversations-list > nav > div.conv-container.ng-star-inserted > mws-conversation-list-item:nth-child(1)'))).click()
            

            # Espera a que aparezca el menú de conversación y sea interactivo antes de hacer clic
            element = WebDriverWait(browser, demora).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'mws-conversation-list-item-menu button[aria-label="Menú de conversación"]'))
            )
            element.click()
            
            # Espera a que aparezca el botón de eliminar y sea interactivo antes de hacer clic
            element = WebDriverWait(browser, demora).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-e2e-conversation-delete] span.mat-mdc-menu-item-text'))
            )
            element.click()
            
            # Espera a que aparezca el botón de confirmar eliminar y sea interactivo antes de hacer clic
            element = WebDriverWait(browser, demora).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-e2e-action-button-confirm].gmat-mdc-button span.mdc-button__label'))
            )
            element.click()
        except:
            browser.quit()
            chrome_service.stop()
            break
        
        

print("Se ha eliminado chat"+str(cont))
