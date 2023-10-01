import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configura el servicio de ChromeDriver
chrome_driver_path = "chromedriver.exe"  # Reemplaza con tu ruta
chrome_service = ChromeService(chrome_driver_path)
chrome_service.start()

# Configura las opciones del navegador
options = webdriver.ChromeOptions()
# Configura opciones adicionales si es necesario

try:
    # Inicializa el WebDriver utilizando el servicio y las opciones
    browser = webdriver.Chrome(service=chrome_service, options=options)

    # Abre la página web
    browser.get('https://messages.google.com/web/conversations')

    # esperar que aparezca el boton de nuevo mensaje
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input")))

    # hacer click en el boton de nuevo mensaje
    browser.find_element(By.CSS_SELECTOR, '#identifierNext > div > button > span').click()

    # hacer click en la entarda de nuevo mensaje
    browser.find_element(By.CSS_SELECTOR, '#identifierNext > div > button > span').click()

    # agregar numero de telefono
    browser.find_element(By.ID, 'identifierId').send_keys("3174466432")
    

    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input")))
    
    browser.find_element(By.CSS_SELECTOR, "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input").send_keys("1007138598")

    browser.find_element(By.CSS_SELECTOR, '#passwordNext > div > button > span').click()

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'identifierId')))



finally:
    # Cierra el navegador y detiene el servicio
    browser.quit()
    chrome_service.stop()
