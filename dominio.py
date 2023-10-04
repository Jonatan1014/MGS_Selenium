from selenium import webdriver
from urllib.parse import urlparse

# Inicializa el navegador
browser = webdriver.Chrome()

# Abre una página web
url = "https://messages.google.com/web/authentication"
browser.get(url)

# Espera un poco para que la página se cargue completamente
browser.implicitly_wait(10)

# Obtiene la URL actual
url_actual = browser.current_url

# Analiza la URL para obtener el dominio
dominio_actual = urlparse(url_actual).netloc

# Imprime el dominio actual
print("Estás en el dominio:", dominio_actual)

# Cierra el navegador
browser.quit()
