import openpyxl
import os
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import easygui as eg
import os
import time
import json

def verRegistro():
    # Cargar el progreso actual desde un archivo o inicializarlo
    progreso = {"fila_actual": 1, "mensaje_actual": 0}
    try:
        with open('progreso.json', 'r') as file:
            progreso = json.load(file)
            return progreso
    except FileNotFoundError:
        pass

def cargaChrome():
    chrome_driver_path = "chromedriver.exe"  # Reemplaza con tu ruta
    chrome_service = ChromeService(chrome_driver_path)

    chrome_service.start()

    # Configura las opciones del navegador
    options = webdriver.ChromeOptions()
    # Configura opciones adicionales si es necesario
    # Deshabilita las notificaciones
    options.add_argument("--disable-notifications")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument(r'user-data-dir=C:\Users\farud\OneDrive\Escritorio\MGS_Selenium\Google')
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
    cont = 0

def programSinImagenes(archivo_excel): 
    
    progreso=verRegistro()
    if verRegistro:
    

    
        libro = openpyxl.load_workbook(archivo_excel)
        hoja = libro["Hoja1"]
        for fila_num, fila in enumerate(hoja.iter_rows(min_row=progreso["fila_actual"], values_only=True), start=progreso["fila_actual"]):
            Celular = " - ".join(map(str, fila))
            if all(cell is None for cell in fila):
                print("Se ha llegado al final del archivo. Proceso detenido.")
                break
            try:
                
                # hacer click en el boton de nuevo mensaje
                browser.find_element(By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-main-nav > div > mw-fab-link > a > span.mdc-button__label').click()

                # hacer click en la entrada de nuevo mensaje
                browser.find_element(By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-new-conversation-container > mw-new-conversation-sub-header > div > div.input-container > mw-contact-chips-input > div > div > input').click()

                # agregar numero de telefono
                browser.find_element(By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-new-conversation-container > mw-new-conversation-sub-header > div > div.input-container > mw-contact-chips-input > div > div > input').send_keys(Celular)

                # seleccionar el numero ingresado
                browser.find_element(By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-new-conversation-container > div > mw-contact-selector-button > button').click()
                
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
                # Si se han enviado 4 mensajes, guarda el progreso y reinicia
                if cont == 2:
                    # Guarda el progreso actual en un archivo
                    progreso["fila_actual"] = fila_num + 1
                    progreso["mensaje_actual"] = MensajeMasivo + 1
                    progreso["cont"] = cont

                    with open('progreso.json', 'w') as file:
                        json.dump(progreso, file)
                        
            except StaleElementReferenceException as e:
                print("Error: Elemento de página obsoleto. ", str(e))
            except ElementClickInterceptedException as e:
                print("Error: Intercepción de clic en el elemento. ", str(e))
            except Exception as e:
                print("Ocurrió un error inesperado: ", str(e))

        
            # Cierra el navegador y detiene el servicio
            time.sleep(3)
            browser.quit()
            chrome_service.stop()
            print("Envio completado")
            libro.close()

archivo_excel =r"C:\Users\farud\OneDrive\Escritorio\MGS_Selenium\pruebas.xlsx"
MensajeMasivo = eg.codebox(msg='Entrada de fuente',
                    title='Control: codebox',
                    )
programSinImagenes(archivo_excel)
