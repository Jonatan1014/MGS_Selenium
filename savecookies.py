import pickle
import undetected_chromedriver as uc
from selenium import webdriver

import time



options = webdriver.ChromeOptions()
options.add_argument("--remote-debugging-port=9222")
options.add_argument(r'--user-data-dir=C:\Users\farud\OneDrive\Escritorio\MGS_Selenium\google')

browser = uc.Chrome(
    options=options,
)
browser.get('https://messages.google.com/web/conversations')


time.sleep(10)

cookies = browser.get_cookies()

pickle.dump(cookies, open("cookies.pkl", "wb"))