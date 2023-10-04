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


os.system('color 1' if os.name == 'nt' else 'clear')

def crearCarpetaGoogle():
    # Obtiene la fecha y hora actual
    now = datetime.now()

    # Formatea la fecha y hora en el formato que desees para la carpeta (año-mes-día_hora-minuto-segundo)
    folder_name = now.strftime("Chrome_%d-%m-%Y_%H-%M-%S")

    # Obtiene la ruta absoluta de la carpeta actual donde está el programa
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Ruta completa para la carpeta dentro de la carpeta actual
    folder_path = os.path.join(current_directory, folder_name)

    # Crea la carpeta
    os.makedirs(folder_path)

    print("Carpeta creada con exito!")
    time.sleep(3)
    return (folder_path)
    
def limpiarcmd():
    os.system('cls' if os.name == 'nt' else 'clear')
 
def interfaz():
    hola = """
         __  __                                  _           _____   __  __    _____ 
        |  \/  |                                (_)         / ____| |  \/  |  / ____|
        | \  / |   ___   _ __    ___    __ _     _    ___  | (___   | \  / | | (___  
        | |\/| |  / _ \ | '_ \  / __|  / _` |   | |  / _ \  \___ \  | |\/| |  \___ \ 
        | |  | | |  __/ | | | | \__ \ | (_| |   | | |  __/  ____) | | |  | |  ____) |
        |_|  |_|  \___| |_| |_| |___/  \__,_|   | |  \___| |_____/  |_|  |_| |_____/ 
                                               _/ |                                  
                                              |__/                                   
        by: JSB
        """
    print(hola)
    
def Bienvenido(duration):
    limpiarcmd()
    chars = ['|', '/', '-', '\\']
    num_chars = len(chars)
    start_time = time.time()
    
    while time.time() - start_time < duration:
        for i in range(num_chars):
            print(f'\rCargando {chars[i]}', end='')
            time.sleep(0.1)
    
    print('\rCarga Completa!   ')
    
    hola = """
         __  __                                  _           _____   __  __    _____ 
        |  \/  |                                (_)         / ____| |  \/  |  / ____|
        | \  / |   ___   _ __    ___    __ _     _    ___  | (___   | \  / | | (___  
        | |\/| |  / _ \ | '_ \  / __|  / _` |   | |  / _ \  \___ \  | |\/| |  \___ \ 
        | |  | | |  __/ | | | | \__ \ | (_| |   | | |  __/  ____) | | |  | |  ____) |
        |_|  |_|  \___| |_| |_| |___/  \__,_|   | |  \___| |_____/  |_|  |_| |_____/ 
                                               _/ |                                  
                                              |__/                                   
        by: JSB
        """
    print(hola)
    chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    num_chars = len(chars)
    start_time = time.time()
    
    while time.time() - start_time < duration:
        for i in range(num_chars):
            print(f'\rIniciando Programa {chars[i]}', end='')
            time.sleep(0.1)
    
    print('\rIniciado Con Exito!   ')
    time.sleep(2)
    
extension1 = ["*.xlsx"]

def envioMensajes(archivo_excel,rutaCarpeta):
    libro = openpyxl.load_workbook(archivo_excel)
    hoja = libro["Hoja1"]
    chrome_driver_path = "chromedriver.exe"  # Reemplaza con tu ruta
    chrome_service = ChromeService(chrome_driver_path)
    chrome_service.start()
    
    # Configura las opciones del navegador
    options = webdriver.ChromeOptions()
    # Configura opciones adicionales si es necesario
    # Deshabilita las notificaciones
    options.add_argument("--disable-notifications")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument('user-data-dir='+rutaCarpeta)


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
    # Cargar el progreso actual desde un archivo o inicializarlo
    progreso = {"fila_actual": 1, "mensaje_actual": 0}
    try:
        with open('progreso.json', 'r') as file:
            progreso = json.load(file)
    except FileNotFoundError:
        pass
    cont = 0
    for fila_num, fila in enumerate(hoja.iter_rows(min_row=progreso["fila_actual"], values_only=True), start=progreso["fila_actual"]):
        # Controlar si hemos llegado al final del archivo
        Celular = " - ".join(map(str, fila))
        if all(cell is None for cell in fila):
            fin_del_archivo = True
            break
        for mensaje_num, parrafo in enumerate(MensajeMasivo.split('\n')[progreso["mensaje_actual"]:], start=progreso["mensaje_actual"]):

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
                
                # Pega el texto en el campo de entrada usando la combinación de teclas "Control + V"
                ActionChains(browser).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                
                # Enviar imagen con Enter
                browser.find_element(By.CSS_SELECTOR, 'mws-autosize-textarea textarea').send_keys(Keys.ENTER)
            except StaleElementReferenceException as e:
                print("Error: Elemento de página obsoleto. ", str(e))
            except ElementClickInterceptedException as e:
                print("Error: Intercepción de clic en el elemento. ", str(e))
            except Exception as e:
                print("Ocurrió un error inesperado: ", str(e))
            
            cont += 1
            print("Mensaje enviado. Total de mensajes enviados:", cont)

            # Si se han enviado 4 mensajes, guarda el progreso y reinicia
            if cont == 2:
                # Guarda el progreso actual en un archivo
                with open('progreso.json', 'w') as file:
                    json.dump({"fila_actual": fila_num + 1, "mensaje_actual": mensaje_num + 1}, file)

                # Cierra el navegador y detiene el servicio
                time.sleep(3)
                browser.quit()
                chrome_service.stop()
                print("Envio completado")

                # Resetea el contador
                cont = 0
    # Elimina el archivo de progreso al finalizar el envío
    try:
        os.remove('progreso.json')
    except FileNotFoundError:
        pass

    libro.close()
    # Si llegamos al final del archivo, detener el proceso
    if fin_del_archivo:
        print("Se ha llegado al final del archivo. Proceso detenido.")
        return


# Programa con envio de imagenes
def program(archivo_excel, rutaCarpeta):            
    libro = openpyxl.load_workbook(archivo_excel)
    hoja = libro["Hoja1"]
    chrome_driver_path = "chromedriver.exe"  # Reemplaza con tu ruta
    chrome_service = ChromeService(chrome_driver_path)
    chrome_service.start()
    
    # Configura las opciones del navegador
    options = webdriver.ChromeOptions()
    # Configura opciones adicionales si es necesario
    # Deshabilita las notificaciones
    options.add_argument("--disable-notifications")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument('user-data-dir='+rutaCarpeta)

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
    # Cargar el progreso actual desde un archivo o inicializarlo
    progreso = {"fila_actual": 1, "mensaje_actual": 0}
    try:
        with open('progreso.json', 'r') as file:
            progreso = json.load(file)
    except FileNotFoundError:
        pass
    
    cont = 0
    for fila_num, fila in enumerate(hoja.iter_rows(min_row=progreso["fila_actual"], values_only=True), start=progreso["fila_actual"]):
        # Controlar si hemos llegado al final del archivo
        Celular = " - ".join(map(str, fila))
        if all(cell is None for cell in fila):
            fin_del_archivo = True
            break
        for mensaje_num, parrafo in enumerate(MensajeMasivo.split('\n')[progreso["mensaje_actual"]:], start=progreso["mensaje_actual"]):

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
                
                # Pega el texto en el campo de entrada usando la combinación de teclas "Control + V"
                ActionChains(browser).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                
                # Enviar imagen con Enter
                browser.find_element(By.CSS_SELECTOR, 'mws-autosize-textarea textarea').send_keys(Keys.ENTER)
            except StaleElementReferenceException as e:
                print("Error: Elemento de página obsoleto. ", str(e))
            except ElementClickInterceptedException as e:
                print("Error: Intercepción de clic en el elemento. ", str(e))
            except Exception as e:
                print("Ocurrió un error inesperado: ", str(e))
            
            cont += 1
            print("Mensaje enviado. Total de mensajes enviados:", cont)

            # Si se han enviado 4 mensajes, guarda el progreso y reinicia
            if cont == 2:
                # Guarda el progreso actual en un archivo
                with open('progreso.json', 'w') as file:
                    json.dump({"fila_actual": fila_num + 1, "mensaje_actual": mensaje_num + 1}, file)

                # Cierra el navegador y detiene el servicio
                time.sleep(3)
                browser.quit()
                chrome_service.stop()
                print("Envio completado")

                # Resetea el contador
                cont = 0

                envioMensajes(archivo_excel,rutaCarpeta)

    

    libro.close()
    # Si llegamos al final del archivo, detener el proceso
    if fin_del_archivo:
        print("Se ha llegado al final del archivo. Proceso detenido.")
        return
    
# Programa sin envio de imagenes
def programSinImagenes(archivo_excel,rutaCarpeta):            

    libro = openpyxl.load_workbook(archivo_excel)
    hoja = libro["Hoja1"]
    chrome_driver_path = "chromedriver.exe"  # Reemplaza con tu ruta
    chrome_service = ChromeService(chrome_driver_path)

    chrome_service.start()

    # Configura las opciones del navegador
    options = webdriver.ChromeOptions()
    # Configura opciones adicionales si es necesario
    # Deshabilita las notificaciones
    options.add_argument("--disable-notifications")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument('user-data-dir='+rutaCarpeta)
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
    for fila in hoja.iter_rows(min_row=1, values_only=True):
        Celular = " - ".join(map(str, fila))
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

def buscar_base_de_datos():
    global BaseDatosMasiva
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    print("Buscar Base de Datos")
    BaseDatosMasiva = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if BaseDatosMasiva:
        print("Base de Datos seleccionada: " + BaseDatosMasiva)
    else:
        salir=str(input("Base de Datos no Seleccionada\n¿Desea salir? y/n\n"))
        limpiarcmd()
        while True:
            try:
                while salir!="y" and salir!="n":
                    salir=str(input("Opcion Invalida\n¿Desea salir? y/n\n"))
                    limpiarcmd()
            except:
                salir=str(input("Base de Datos no Seleccionada\n¿Desea salir? y/n\n"))
            else:
                if salir=="y":
                    break
                else:
                    buscar_base_de_datos()
                    
                
                
        buscar_base_de_datos()

def validarMensaje():
    mensaje = str(input("El mensaje es correcto? y/n "))
    while True:
        try:
            while mensaje!="y" and mensaje!="n":
                mensaje = str(input("El mensaje es correcto? y/n "))
        except:
            mensaje = str(input("El mensaje es correcto? y/n "))
        else:
            if mensaje=="y":
                return True
            else:
                return False
    
def introducir_mensaje():
    global MensajeMasivo
    MensajeMasivo = eg.codebox(msg='Entrada de fuente',
                    title='Control: codebox',
                    )
    if MensajeMasivo:
        print("Mensaje escrito: " + MensajeMasivo)
        mensaje=validarMensaje()
        if not mensaje:
            introducir_mensaje()

def validarImagen():
    imagen = str(input("Desea Enviar Imagen? y/n: "))
    while True:
        try:
            while imagen!="y" and imagen!="n":
                imagen = str(input("Desea Enviar Imagen? y/n: "))
        except:
            imagen = str(input("Desea Enviar Imagen? y/n: "))
        else:
            if imagen=="y":
                return True
            else:
                return False
                n
                
def Menu():
    Bienvenido(1)
    buscar_base_de_datos()
    time.sleep(1)
    limpiarcmd()
    interfaz()
    image=validarImagen()
    time.sleep(1)
    limpiarcmd()
    interfaz()
    if image:
        introducir_mensaje()
        time.sleep(1)
        limpiarcmd()
        interfaz()
        try:
            if BaseDatosMasiva and MensajeMasivo:
                rutaCarpeta=crearCarpetaGoogle()
                program(BaseDatosMasiva,rutaCarpeta)
        except:
            print("Complete todos los campos antes de comenzar.")
    else:
        introducir_mensaje()
        time.sleep(1)
        limpiarcmd()
        interfaz()
        try:
            if BaseDatosMasiva and MensajeMasivo:
                rutaCarpeta=crearCarpetaGoogle()
                programSinImagenes(BaseDatosMasiva, rutaCarpeta)
        except:
            print("Complete todos los campos antes de comenzar.")
Menu()