import webbrowser as web
import time
import openpyxl
from timeit import default_timer
import threading
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException

import time


extension1 = ["*.xlsx"]
extension2 = ["*.jpg", "*.png"]
extension3 = [".jpg", ".png"]
enviados = []
inicio = 1
detener_programa = False  # Variable para detener el programa

class ProgressWindow:
    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Progreso")
        self.progress_label = tk.Label(self.top, text="Interacciones realizadas: 0")
        self.progress_label.pack(padx=10, pady=10)
        self.stop_button = tk.Button(self.top, text="Detener", command=self.detener)
        self.stop_button.pack(padx=10, pady=10)
        self.top.attributes("-topmost", True)  # Establece la ventana como una ventana superior
        self.top.withdraw()  # Oculta la ventana al principio

    def show(self):
        self.top.deiconify()

    def hide(self):
        self.top.withdraw()

    def update_progress(self, count):
        self.progress_label.config(text=f"Interacciones realizadas: {count}")

    def detener(self):
        global detener_programa
        detener_programa = True
        self.hide()
        messagebox.showinfo("Detener", "El programa ha sido detenido.")

def seleccionar_imagenes():
    images = []
    msg = "Seleccione imágenes para enviar"
    title = "Buscar Imágenes"
    filetypes = extension2

    while True:
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png")])
        if filepath == '':
            break
        else:
            _, extension = os.path.splitext(filepath)
            if extension.lower() in extension3:
                images.append(filepath)
            else:
                messagebox.showerror("Error", f"La imagen '{filepath}' no tiene una extensión válida. Por favor, seleccione imágenes con extensiones .jpg o .png.")

    return images
# Programa sin envio de imagenes
def programSinImage(archivo_excel, mensaje, progress_window):

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

            # escribir mensaje 
            browser.find_element(By.CSS_SELECTOR,'mws-autosize-textarea textarea').send_keys(mensaje)

            # enviar mensaje con enter
            browser.find_element(By.CSS_SELECTOR,'mws-autosize-textarea textarea').send_keys(Keys.ENTER)
            # hacer click en el boton de nuevo mensaje
            browser.find_element(By.CSS_SELECTOR, 'body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-main-nav > div > mw-fab-link > a').click()
                
        except StaleElementReferenceException as e:
            print("Error: Elemento de página obsoleto. ", str(e))
        except ElementClickInterceptedException as e:
            print("Error: Intercepción de clic en el elemento. ", str(e))
        except Exception as e:
            print("Ocurrió un error inesperado: ", str(e))

    
    # Cierra el navegador y detiene el servicio
    browser.quit()
    chrome_service.stop()
    print("Envio completado")
        
    libro.close()


def buscar_base_de_datos():
    global BaseDatosMasiva
    BaseDatosMasiva = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if BaseDatosMasiva:
        base_datos_label.config(text="Base de Datos seleccionada: " + BaseDatosMasiva)

def introducir_mensaje():
    global MensajeMasivo
    MensajeMasivo = mensaje_entry.get()
    if MensajeMasivo:
        mensaje_label.config(text="Mensaje escrito: " + MensajeMasivo)

def buscar_imagen():
    global ImagenMasiva
    ImagenMasiva = seleccionar_imagenes()
    if ImagenMasiva:
        imagen_label.config(text="Imagen seleccionada: " + str(len(ImagenMasiva)))

def comenzar():
    global detener_programa
    detener_programa = False  # Reinicia la variable de detención
    
    try:
        if BaseDatosMasiva and MensajeMasivo:
            
            t = threading.Thread(target=programSinImage, args=(BaseDatosMasiva, MensajeMasivo, progress_window))
            
        
    except:
        informacion_label.config(text="Complete todos los campos antes de comenzar.")

    else:
        t = threading.Thread(target=programSinImage, args=(BaseDatosMasiva, MensajeMasivo, progress_window))
        t.start()



# Crear la ventana principal
root = tk.Tk()
root.title("Mensajería Masiva")

# Crear y configurar widgets
base_datos_button = tk.Button(root, text="Buscar Base de Datos", command=buscar_base_de_datos)
base_datos_button.pack(pady=10)

base_datos_label = tk.Label(root, text="", fg="green")
base_datos_label.pack()

mensaje_label = tk.Label(root, text="", fg="green")
mensaje_label.pack()

mensaje_entry = tk.Entry(root, width=50)
mensaje_entry.pack()

mensaje_button = tk.Button(root, text="Introducir Mensaje", command=introducir_mensaje)
mensaje_button.pack()

imagen_label = tk.Label(root, text="", fg="green")
imagen_label.pack()

imagen_button = tk.Button(root, text="Buscar Imagen", command=buscar_imagen)
imagen_button.pack()

comenzar_button = tk.Button(root, text="Comenzar", command=comenzar)
comenzar_button.pack(pady=10)

informacion_label = tk.Label(root, text="", fg="red")
informacion_label.pack(pady=10)

# Ventana de progreso
progress_window = ProgressWindow(root)

# Ejecutar la aplicación
root.mainloop()
