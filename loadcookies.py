import pickle
import undetected_chromedriver as uc
import time



browser = uc.Chrome()
browser.get('https://messages.google.com/web/conversations')

cookies = pickle.load(open("cookies.pkl", "rb"))

for cookie in cookies:
    cookie['domain'] = "messages.google.com"
    
    try:
        browser.add_cookie(cookie)
    except Exception as e:
        print(e)

browser.get('https://messages.google.com/web/conversations/new')

time.sleep(120)