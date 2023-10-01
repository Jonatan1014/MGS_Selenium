import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
options = uc.ChromeOptions()

browser = uc.Chrome(options=options)

# Obtén las cookies antes de cargar la página
browser.get('https://messages.google.com/web/conversations')
cookies_before_login = browser.get_cookies()
print("Cookies antes de inicio de sesión:", cookies_before_login)

# Inicia sesión
browser.find_element(By.CSS_SELECTOR, 'a.fab').click()
# browser.find_element(By.CSS_SELECTOR, '#identifierNext > div > button > span').send_keys(email)

time.sleep(6)
password_selector = "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input"

WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, password_selector)))

# browser.find_element(By.CSS_SELECTOR, password_selector).send_keys(password)
# browser.find_element(By.CSS_SELECTOR, '#passwordNext > div > button > span').click()

# Espera a que la página se cargue completamente (ajusta el tiempo según sea necesario)
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'identifierId')))

# Añade una nueva cookie después del inicio de sesión
new_cookie = {'name': 'mi_cookie', 'value': '12345', 'domain': '.google.com'}
browser.add_cookie(new_cookie)

# Obtén las cookies después de añadir una nueva cookie
cookies_after_login = browser.get_cookies()
print("Cookies después de añadir una cookie:", cookies_after_login)

# Cierra el navegador
browser.quit()
