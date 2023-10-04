import unittest
from pyunitreport import HTMLTestRunner
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class Save(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument(r'user-data-dir=./google')

        self.driver = webdriver.Chrome(options=options)
        driver = self.driver

    
    def test_open_page(self):
        try:
            driver = self.driver

            url = "https://messages.google.com/web/conversations"
            driver.get(url)
            time.sleep(20)
        except:
            print("bye")
            
    def tearDown(self):
        self.driver.quit()


if __name__== '__main__':
    unittest.main(verbosity=2, testRunner = HTMLTestRunner(output = 'reports', report_name = 'saveSession'))